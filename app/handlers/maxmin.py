from . import Handler
from shutil import rmtree
from app import chpc
from app.params import *
import re
from numpy import random
import numpy
from app import tweak
import logging


class MaxMin(Handler):
    TYPE_MIN = 'min'
    TYPE_MAX = 'max'

    TYPES = [TYPE_MAX, TYPE_MIN]

    def make(self, base=None):
        pass

    def submit(self):
        self.make_files()
        self.upload_files()
        self.submit_all_jobs()

        self.set_status(self.STATE_SUBMITTED)

    def abandon(self):
        self.sample.status = self.STATE_ERROR
        self.sample.has_done = 1

    def pull(self):
        print('pulling... %s' % self.sample.id)
        jobs = self.fetch_jobs()
        print(jobs)
        if len(jobs) > 0:
            self.describe_jobs(jobs)
            raise self.StillRunning()
        else:
            finished = self.finished_jobs()
            print('meep finished: [%s]' % ', '.join(finished))

            if len(finished) < 2:
                if self.sample.retried > 3:
                    raise self.FatalError()
                else:
                    logging.info('job was interrupted')
                    raise self.Interrupted()

    def rate(self):
        print('calling matlab')
        self.call_matlab()

        loss = {}
        for m_type in ['min', 'max']:
            loss[m_type] = self.fetch_matlab_result(m_type)

        if not self.calculate_rating(loss['max'], loss['min']):
            self.sample.status = self.STATE_ERROR
            self.sample.has_done = 1
            print('error')
        else:
            self.sample.status = self.STATE_DONE
            self.sample.has_done = 1
            print('done')

    def restart(self):
        logging.info('restarting job')
        finished = self.finished_jobs()
        self.make_files()
        self.upload_files()
        self.restart_failed_jobs(finished)

    def restart_failed_jobs(self, finished):
        for m_type in self.TYPES:
            if m_type not in finished:
                self.submit_job(m_type)

        self.sample.retried += 1

    def set_status(self, status):
        self.sample.status = status

    def make_files(self):
        self.make_meep_files()
        self.make_matlab_files()
        self.make_sbatch_files()

    def submit_all_jobs(self):
        self.submit_job(self.TYPE_MAX)
        self.submit_job(self.TYPE_MIN)

    def make_matlab_files(self):
        self.write_file('matlab.sh', self.render_tpl('matlab', {
            '__LAYOUT_LENGTH__': self.config['length'],
            '__LAYOUT_WIDTH__': self.config['width'],
            '__MATLAB_NAME__': self.config['matlab']
        }))
        self.write_file('xy.py', self.render_tpl('xy'))

    def make_sbatch_files(self):
        time_cost = self.config['time']

        for m_type in self.TYPES:
            content = self.render_tpl('sbatch', {
                '__NAME__': '%s-%s' % (self.sample.job_name, m_type),
                '__ROOT_DIR__': CHPC_WORK_DIR,
                '__SUB_DIR__': self.sample.digest,
                '__ACCOUNT__': SBATCH_ACCOUNT,
                '__PARTITION__': SBATCH_PARTITION,
                '__MAX_MIN__': m_type,
                '__TIME__': time_cost
            })
            self.write_file('sbatch-%s.sh' % m_type, content)

    def make_meep_files(self):

        whole_width = self.config['width']
        whole_length = self.config['length']

        l_input = self.config['meep_linput']
        l_output = self.config['meep_loutput']

        for min_max in self.TYPES:
            header = self.render_tpl('meep-%s-header' % min_max, {
                '__PIXEL_LENGTH__': whole_length / 10,
                '__PIXEL_WIDTH__': whole_width / 10,
                '__GRAPH_LENGTH__': self.config['graphene_length'],
                '__RESOLUTION__': RESOLUTION,
                '__LAYOUT_LENGTH__': whole_length,
                '__LAYOUT_WIDTH__': whole_width,
                '__L_INPUT__': l_input,
                '__L_OUTPUT__': l_output,
                '__INPUT_WAVEGUIDE__': self.config['meep_input_waveguide']
            })
            points = []

            for part_name, part_points in self.sample.parts.items():
                part_cfg = self.config['parts'][part_name]
                layout = numpy.array(part_points).reshape((part_cfg['width']['size'], part_cfg['length']['size']))

                width_offset = part_cfg['width']['offset']
                length_offset = part_cfg['length']['offset']

                for r in range(0, len(layout)):
                    row = layout[r]
                    for c in range(0, len(row)):
                        if int(row[c]) == 1:
                            points.append(self.render_tpl('meep-point', {
                                '__LENGTH_OFFSET__': c + 1 + length_offset,
                                '__WIDTH_OFFSET__': r + 1 + width_offset,
                            }))

            points = "\n\n".join(points)
            footer = self.render_tpl('meep-%s-footer' % min_max, {
                '__OUTPUT_WAVEGUIDE__': self.config['meep_output_waveguide'],
                '__EZ__': self.config['meep_ez']
            })
            content = header + points + footer
            self.write_file('meep-' + min_max + '.ctl', content)

    def run_matlab(self):
        chpc.remote_shell_file('/'.join([CHPC_WORK_DIR, self.sample.digest, 'matlab.sh']))

    def get_loss_value(self, m_type):
        file = '/'.join([CHPC_WORK_DIR, self.sample.digest, 'loss-%s.txt']) % m_type
        out = chpc.remote_cmd('cat %s' % file)
        matched = re.match("^\d+\.\d+$", out)
        if matched is not None:
            return float(matched.group(0))
        else:
            return None

    def restart_all(self):
        chpc.remote_cmd('rm -rf %s/%s/*.log' % (CHPC_WORK_DIR, self.sample.digest))

    def clean(self):
        rmtree(self.local_sample_folder)

    def clean_remote(self):
        chpc.remote_cmd('rm -rf %s/%s' % (CHPC_WORK_DIR, self.sample.digest))

    def call_matlab(self):
        chpc.remote_cmd('/bin/bash %s/matlab.sh' % self.remote_sample_folder)

    def fetch_all_matlab_results(self):
        losses = {}

        for m_type in self.TYPES:
            losses[m_type] = self.fetch_matlab_result(m_type)

        return losses

    def fetch_matlab_result(self, m_type):
        chpc.remote_cmd('/usr/bin/python %s/xy.py' % self.remote_sample_folder)

        out = chpc.remote_cmd('cat %s/loss-%s.txt' % (self.remote_sample_folder, m_type))
        out = str(out).strip()
        matched = re.match('.*\s*(\d+\.\d+)\s*.*', out, re.MULTILINE)
        if matched is not None:
            return float(matched.group(1))
        else:
            return None

    def finished_jobs(self):
        finished = []
        for m_type in ['min', 'max']:
            if self.is_type_done(m_type):
                finished.append(m_type)

        return finished

    def is_type_done(self, m_type):
        output = chpc.remote_cmd('ls -l %s/meep-%s-out/hx-000200.00.h5' % (self.remote_sample_folder, m_type))
        if len(output) > 0:
            return 'No such file or directory' not in output
        else:
            return False

    def calculate_rating(self, loss_max, loss_min):
        if not loss_max or not loss_min:
            return False

        results = {
            'loss_max': loss_max,
            'loss_min': loss_min,
            'depth': (loss_max - loss_min) / (loss_max + loss_min) * 100
        }

        loss_min_target = 0.05

        if loss_min < loss_min_target:
            g = 0
        else:
            g = ((loss_min_target - loss_min) / loss_min_target) ** 2

        self.sample.rating = round(((loss_max - loss_min) / loss_max) ** 2 - g, 5)

        self.sample.results = results

        return True

    def create_parts(self, parent):
        category_params = self.config

        new_parts = {}
        for part_name, part_cfg in category_params['parts'].items():
            tweak_module = getattr(tweak, category_params['parts'][part_name]['tweak'])
            tweak_method = getattr(tweak_module, 'tweak')

            if part_name in parent.parts:
                old_part = parent.parts[part_name]
            else:
                part_width = part_cfg['width']['size']
                part_length = part_cfg['length']['size']
                old_part = [random.randint(2) for _ in range(part_width * part_length)]

            new_parts[part_name] = tweak_method(old_part, part_cfg)

        return new_parts
