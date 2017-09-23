import yaml
from app.params import *
from os import path, makedirs
from app.db import session
from app import chpc
import logging


class Handler:
    STATE_READY = 'ready'
    STATE_SUBMITTED = 'submitted'
    STATE_DONE = 'done'
    STATE_ERROR = 'error'

    sample = None
    config = {}

    def __init__(self, sample):
        self.sample = sample

        if self.sample.status is None:
            self.sample.status = self.STATE_READY

        self.local_data_folder = path.abspath(path.join(path.expanduser('~'), 'Documents', 'meep-data'))
        self.local_sample_folder = path.join(self.local_data_folder, self.sample.id)
        self.remote_data_folder = CHPC_WORK_DIR
        self.remote_sample_folder = path.join(self.remote_data_folder, self.sample.id)
        self.tpl_folder = path.abspath(path.join(path.dirname(__file__), '..', '..', 'templates'))

        if not path.isdir(self.local_sample_folder):
            makedirs(self.local_sample_folder, exist_ok=True)

        self.load_config()

    def work(self):
        status = self.sample.status

        if status == self.STATE_READY:
            self.submit()
        elif status == self.STATE_SUBMITTED:
            try:
                self.pull()
                self.rate()
            except self.StillRunning:
                pass
            except self.Interrupted:
                self.restart()
            except self.FatalError:
                self.abandon()
                self.set_status(self.STATE_ERROR)
            except Exception as e:
                print(e)
        elif status == self.STATE_ERROR:
            pass
        else:
            raise RuntimeError('unknown status')

        session.add(self.sample)
        session.commit()

    class StillRunning(Exception):
        pass

    class Interrupted(Exception):
        pass

    class FatalError(Exception):
        pass

    def load_config(self):
        filename = path.join(path.dirname(__file__), '..', 'configs', self.sample.category) + '.yml'
        with open(filename) as f:
            self.config = yaml.safe_load(f)

    def make(self, base=None):
        raise NotImplementedError()

    def fetch(self):
        pass

    def restart(self):
        raise NotImplementedError()

    def abandon(self):
        raise NotImplementedError()

    def submit(self):
        raise NotImplementedError()

    def pull(self):
        raise NotImplementedError()

    def rate(self):
        raise NotImplementedError()

    def set_status(self, status):
        self.sample.status = status

    def template(self, name, variables=None):
        template_file = path.join(self.tpl_folder, self.config['prefix'], name + '.txt')

        with open(template_file, 'r') as f:
            content = f.read()
        if variables is not None:
            for k, v in variables.items():
                content = content.replace('{%s}' % k, str(v))
        return content

    def upload_files(self):
        chpc.rsync(self.local_sample_folder, self.remote_data_folder)

    def create_file(self, filename, content):
        open(path.join(self.local_sample_folder, filename), 'w+').write(content)

    def submit_job(self, job_name):
        sbatch_file = path.join(self.remote_sample_folder, 'sbatch-{0}.sh'.format(job_name))
        chpc.sbatch(sbatch_file)

    def fetch_jobs(self):
        return chpc.squeue(self.sample.job_name)

    @staticmethod
    def describe_jobs(jobs):
        for job in jobs:
            if job['state'] == 'PD':
                logging.info('job %s %s [PD], expect start at %s' % (job['job_id'], job['job_name'], job['time_expect']))
            else:
                logging.info('job %s %s [%s], time used %s' % (job['job_id'], job['job_name'], job['state'], job['time_used']))


