from os import path, makedirs
from app.params import *
from app import chpc
import re
from shutil import rmtree
import numpy

ROOT_DIR = path.join(path.dirname(__file__), '..')
LOCAL_DATA_DIR = path.abspath(path.join(path.expanduser('~'), 'Documents', 'meep-data'))
TPL_DIR = path.abspath(path.join(ROOT_DIR, 'templates'))


class Handler:
    TYPE_MIN = 'min'
    TYPE_MAX = 'max'

    TYPES = [TYPE_MAX, TYPE_MIN]

    def __init__(self, sample):
        self.sample = sample
        self.digest = sample.digest
        self.folder = path.join(LOCAL_DATA_DIR, self.digest)
        if not path.isdir(self.folder):
            makedirs(self.folder, exist_ok=True)

        self.category_cfg = CATEGORIES[self.sample.category]

    def make_program_files(self):
        self.make_meep_files()
        self.make_matlab_files()
        self.make_sbatch_files()

    def upload_program_files(self):
        self.rsync_program_files()

    def submit_all(self):
        self.submit_job(self.TYPE_MAX)
        self.submit_job(self.TYPE_MIN)

    def submit_job(self, m_type):
        chpc.sbatch('/'.join([CHPC_WORK_DIR, self.digest, 'sbatch-%s.sh' % m_type]))

    def fetch_jobs(self):
        return chpc.squeue('meep-%i' % self.sample.id)

    def rsync_program_files(self):
        chpc.rsync(self.folder, CHPC_WORK_DIR + '/')

    def make_matlab_files(self):
        self.output('matlab.sh', self.render('matlab', {
            '__LAYOUT_LENGTH__': self.category_cfg['length'],
            '__LAYOUT_WIDTH__': self.category_cfg['width'],
            '__MATLAB_NAME__': self.category_cfg['matlab']
        }))
        self.output('xy.py', self.render('xy'))

    def make_sbatch_files(self):
        category_params = CATEGORIES[self.sample.category]
        time_cost = category_params['time']

        for m_type in self.TYPES:
            content = self.render('sbatch', {
                '__NAME__': 'meep-%i-%s' % (self.sample.id, m_type),
                '__ROOT_DIR__': CHPC_WORK_DIR,
                '__SUB_DIR__': self.digest,
                '__ACCOUNT__': SBATCH_ACCOUNT,
                '__PARTITION__': SBATCH_PARTITION,
                '__MAX_MIN__': m_type,
                '__TIME__': time_cost
            })
            self.output('sbatch-%s.sh' % m_type, content)

    def make_meep_files(self):
        category_params = CATEGORIES[self.sample.category]

        whole_width = category_params['width']
        whole_length = category_params['length']

        l_input = category_params['meep_linput']
        l_output = category_params['meep_loutput']

        for min_max in self.TYPES:
            header = self.render('meep-%s-header' % min_max, {
                '__PIXEL_LENGTH__': whole_length / 10,
                '__PIXEL_WIDTH__': whole_width / 10,
                '__GRAPH_LENGTH__': category_params['graphene_length'],
                '__RESOLUTION__': RESOLUTION,
                '__LAYOUT_LENGTH__': whole_length,
                '__LAYOUT_WIDTH__': whole_width,
                '__L_INPUT__': l_input,
                '__L_OUTPUT__': l_output,
                '__INPUT_WAVEGUIDE__': category_params['meep_input_waveguide']
            })
            points = []

            for part_name, part_points in self.sample.parts.items():
                part_cfg = category_params['parts'][part_name]
                layout = numpy.array(part_points).reshape((part_cfg['width']['size'], part_cfg['length']['size']))

                width_offset = part_cfg['width']['offset']
                length_offset = part_cfg['length']['offset']

                for r in range(0, len(layout)):
                    row = layout[r]
                    for c in range(0, len(row)):
                        if int(row[c]) == 1:
                            points.append(self.render('meep-point', {
                                '__LENGTH_OFFSET__': c + 1 + length_offset,
                                '__WIDTH_OFFSET__': r + 1 + width_offset,
                            }))

            points = "\n\n".join(points)
            footer = self.render('meep-%s-footer' % min_max, {
                '__OUTPUT_WAVEGUIDE__': category_params['meep_output_waveguide'],
                '__EZ__': category_params['meep_ez']
            })
            content = header + points + footer
            self.output('meep-' + min_max + '.ctl', content)

    @staticmethod
    def render(name, variables=None):
        with open(path.join(TPL_DIR, name + '.tpl'), 'r') as f:
            content = f.read()
        if variables is not None:
            for k, v in variables.items():
                content = content.replace('{%s}' % k, str(v))
        return content

    def output(self, filename, content):
        open(path.join(self.folder, filename), 'w+').write(content)

    def fetch_type_is_done(self, m_type):
        output = chpc.remote_cmd('ls -l %s/%s/has-done-%s.lock' % (CHPC_WORK_DIR, self.digest, m_type))
        if len(output) > 0:
            return 'No such file or directory' not in output
        else:
            return False

    def run_matlab(self):
        chpc.remote_shell_file('/'.join([CHPC_WORK_DIR, self.digest, 'matlab.sh']))

    def get_loss_value(self, m_type):
        file = '/'.join([CHPC_WORK_DIR, self.digest, 'loss-%s.txt']) % m_type
        out = chpc.remote_cmd('cat %s' % file)
        matched = re.match("^\d+\.\d+$", out)
        if matched is not None:
            return float(matched.group(0))
        else:
            return None

    def submit_again(self, m_type):
        chpc.remote_cmd('rm -rf %s/%s/*-%s.log' % (CHPC_WORK_DIR, self.digest, m_type))
        self.submit_job(m_type)

    def restart_all(self):
        chpc.remote_cmd('rm -rf %s/%s/*.log' % (CHPC_WORK_DIR, self.digest))

    def clean(self):
        rmtree(path.join(LOCAL_DATA_DIR, self.digest))

    def clean_remote(self):
        chpc.remote_cmd('rm -rf %s/%s' % (CHPC_WORK_DIR, self.digest))

    def call_matlab(self):
        chpc.remote_cmd('/bin/bash %s/%s/matlab.sh' % (CHPC_WORK_DIR, self.digest))

    def fetch_all_matlab_results(self):
        losses = {}

        for m_type in self.TYPES:
            losses[m_type] = self.fetch_matlab_result(m_type)

        return losses

    def fetch_matlab_result(self, m_type):
        chpc.remote_cmd('/usr/bin/python %s/%s/xy.py' % (CHPC_WORK_DIR, self.digest))

        out = chpc.remote_cmd('cat %s/%s/loss-%s.txt' % (CHPC_WORK_DIR, self.digest, m_type))
        out = str(out).strip()
        matched = re.match('.*\s*(\d+\.\d+)\s*.*', out, re.MULTILINE)
        if matched is not None:
            return float(matched.group(1))
        else:
            return None
