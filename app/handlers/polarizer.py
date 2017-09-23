from . import Handler
from app.params import *
import numpy
import logging
from app import chpc
from hashlib import md5
from random import randint, random


class Polarizer(Handler):
    def make(self, base=None):
        raise NotImplementedError()

    def fetch(self):
        pass

    def restart(self):
        logging.info('restarting job')
        self.make_files()
        self.upload_files()
        self.submit_job('main')

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
        self.sample.results = {
            'result': result
        }

        self.sample.rating = -numpy.log(numpy.sqrt((result['eyt'] - 0.028) ** 2 + result['ezt'] ** 2 + result['ext'] ** 2))

    def make_files(self):
        self.make_meep_files()
        self.make_matlab_files()
        self.make_sbatch_files()

    def make_matlab_files(self):
        self.create_file('matlab.sh', self.template('polarizer-matlab', {
            '__MATLAB_NAME__': self.config['matlab']
        }))
        # self.write_file('xy.py', self.render_tpl('xy'))

    def make_meep_files(self):
        header = self.template('polarizer-meep-header')
        footer = self.template('polarizer-meep-footer')

        points = []
        layout = numpy.array(self.sample.parts).reshape((self.config['y_length'], self.config['z_length']))

        for row_index in range(0, len(layout)):
            row = layout[row_index]
            for col_index in range(0, len(row)):
                points.append(self.template('polarizer-meep-point', {
                    '__Y__': col_index + 1,
                    '__Z__': row_index + 1,
                    '__X__': row[col_index]
                }))

        points = "\n\n".join(points)

        content = header + points + footer
        self.create_file('meep.ctl', content)

    def make_sbatch_files(self):
        content = self.template('polarizer-sbatch', {
            '__NAME__': self.sample.job_name,
            '__WORKDIR__': self.remote_sample_folder,
            '__ACCOUNT__': SBATCH_ACCOUNT,
            '__PARTITION__': SBATCH_PARTITION,
            '__TIME__': self.config['time']
        })
        self.create_file('sbatch-main.sh', content)

    def is_job_done(self):
        output = chpc.remote_cmd('ls -l %s/meep-out/hx-000001000.h5' % self.remote_sample_folder)
        if len(output) > 0:
            return 'No such file or directory' not in output
        else:
            return False

    def call_matlab(self):
        chpc.remote_cmd('/bin/bash %s/matlab.sh' % self.remote_sample_folder)

    def fetch_matlab_result(self):
        out = chpc.remote_cmd('cat %s/results.csv' % self.remote_sample_folder)
        out = str(out).strip()
        data = {}
        for item in out.split(','):
            name, value = item.split(":")
            data[name] = float(value)

        return data

    def generate_child(self):
        from app.sample import Sample
        sample = Sample()
        sample.parent_id = self.sample.id
        sample.category = self.sample.category
        sample.defect = 0
        sample.parts = self.mutate_parts(self.sample.parts)
        sample.digest = self.calculate_digest(sample)

        return sample

    @staticmethod
    def calculate_digest(sample):
        return md5(','.join(str(p) for p in sample.parts).encode('utf-8')).hexdigest()

    def mutate_parts(self, parts):
        row = randint(0, 15)
        col = randint(0, 15)

        layout = numpy.array(parts).reshape((self.config['y_length'], self.config['z_length']))

        for row_index in range(row, row + 4):
            for col_index in range(col, col + 4):
                if random() > 0.5:
                    original_value = layout[row_index][col_index]
                    tweaked_value = original_value + randint(-20, 20) * 50
                    if tweaked_value < 0:
                        tweaked_value = 0
                    layout[row_index][col_index] = tweaked_value

        return layout.flatten().tolist()
