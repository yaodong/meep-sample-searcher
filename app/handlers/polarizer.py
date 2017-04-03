from . import Handler
from app.params import *
import numpy, logging
from app import chpc
import re


class Polarizer(Handler):
    def make(self, base=None):
        raise NotImplementedError()

    def fetch(self):
        pass

    def restart(self):
        raise NotImplementedError()

    def abandon(self):
        raise NotImplementedError()

    def submit(self):
        self.make_files()
        self.upload_files()
        self.submit_job('main')

        self.set_status(self.STATE_SUBMITTED)

    def pull(self):
        logging.info('pulling...')
        jobs = self.fetch_jobs()

        if len(jobs) > 0:
            self.describe_jobs(jobs)
            raise self.StillRunning()
        else:
            if not self.is_job_done():
                if self.sample.retried > 3:
                    raise self.FatalError()
                else:
                    raise self.Interrupted()

    def rate(self):
        logging.info('calling matlab')
        self.call_matlab()

        result = self.fetch_matlab_result()

        self.sample.status = self.STATE_DONE
        self.sample.has_done = 1
        self.sample.rating = result * 1e5
        self.sample.results = {
            'result': result
        }

    def make_files(self):
        self.make_meep_files()
        self.make_matlab_files()
        self.make_sbatch_files()

    def make_matlab_files(self):
        self.write_file('matlab.sh', self.render_tpl('polarizer-matlab', {
            '__MATLAB_NAME__': self.config['matlab']
        }))
        # self.write_file('xy.py', self.render_tpl('xy'))

    def make_meep_files(self):
        header = self.render_tpl('polarizer-meep-header')
        footer = self.render_tpl('polarizer-meep-footer')

        points = []

        for part_name, part_points in self.sample.parts.items():
            part_cfg = self.config['parts'][part_name]
            layout = numpy.array(part_points).reshape((part_cfg['y']['size'], part_cfg['z']['size']))

            y_offset = part_cfg['y']['offset']
            z_offset = part_cfg['z']['offset']

            for r in range(0, len(layout)):
                row = layout[r]
                for c in range(0, len(row)):
                    if int(row[c]) == 1:
                        points.append(self.render_tpl('polarizer-meep-point', {
                            '__Y__': c + 1 + y_offset,
                            '__Z__': r + 1 + z_offset,
                        }))

        points = "\n\n".join(points)

        content = header + points + footer
        self.write_file('meep.ctl', content)

    def make_sbatch_files(self):
        content = self.render_tpl('polarizer-sbatch', {
            '__NAME__': self.sample.job_name,
            '__WORKDIR__': self.remote_sample_folder,
            '__ACCOUNT__': SBATCH_ACCOUNT,
            '__PARTITION__': SBATCH_PARTITION,
            '__TIME__': self.config['time']
        })
        self.write_file('sbatch-main.sh', content)

    def is_job_done(self):
        output = chpc.remote_cmd('ls -l %s/meep-out/hx-000300.00.h5' % self.remote_sample_folder)
        if len(output) > 0:
            return 'No such file or directory' not in output
        else:
            return False

    def call_matlab(self):
        # chpc.remote_cmd('/bin/bash %s/matlab.sh' % self.remote_sample_folder)
        pass

    def fetch_matlab_result(self):
        out = chpc.remote_cmd('cat %s/results.txt' % self.remote_sample_folder)
        out = str(out).strip()
        number = re.sub("[^e0-9-.]+", "", out, flags=re.IGNORECASE | re.MULTILINE)
        return float(number)
