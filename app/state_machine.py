from app.handler import Handler
from app.db import session


class StateMachine:
    STATE_READY = 'ready'
    STATE_SUBMITTED = 'submitted'
    STATE_QUEUE = 'queue'
    STATE_MATLAB = 'matlab'
    STATE_RATING = 'rating'
    STATE_DONE = 'done'
    STATE_ERROR = 'error'

    def __init__(self, sample):
        self.sample = sample
        self.status = None

        if sample.status is None:
            sample.status = self.STATE_READY

        self.handler = Handler(self.sample)

    @property
    def current_status(self):
        return self.sample.status

    @current_status.setter
    def current_status(self, value):
        self.sample.status = value

    def work(self):
        self.output_summary()

        action = getattr(self, 'when_' + self.current_status)
        action()
        session.add(self.sample)
        session.commit()

    def when_ready(self):
        print('generating files')
        self.handler.make_program_files()

        print('uploading files')
        self.handler.upload_program_files()

        print('submitting task')
        self.handler.submit_all()
        self.current_status = self.STATE_SUBMITTED

    def when_submitted(self):
        print('checking job status')
        jobs = self.handler.fetch_jobs()
        if len(jobs) > 0:
            self.describe_jobs(jobs)
        else:
            finished = self.finished_jobs()
            print('meep finished: %s' % ', '.join(finished))
            if len(finished) == 2:
                self.current_status = self.STATE_RATING
            else:
                print('re-making')
                self.handler.make_program_files()
                print('re-uploading')
                self.handler.upload_program_files()
                print('re-starting')
                self.restart_failed_jobs(finished)

    def when_rating(self):
        print('calling matlab')
        self.handler.call_matlab()

        for m_type in ['min', 'max']:
            loss = self.handler.fetch_matlab_result(m_type)
            setattr(self.sample, 'loss_%s' % m_type, loss)

        if not self.sample.rate():
            self.current_status = self.STATE_ERROR
            self.sample.has_done = 1
            print('error')
        else:
            self.current_status = self.STATE_DONE
            self.sample.has_done = 1
            print('done')
            self.handler.clean()

    def when_error(self):
        self.sample.has_done = 1

    @staticmethod
    def describe_jobs(jobs):
        for job in jobs:
            if job['state'] == 'PD':
                print('job %s %s [PD], expect start at %s' % (job['job_id'], job['job_name'], job['time_expect']))
            else:
                print('job %s %s [%s], time used %s' % (job['job_id'], job['job_name'], job['state'], job['time_used']))

    def restart_failed_jobs(self, finished):
        if self.sample.retried > 3:
            self.current_status = self.STATE_ERROR
            return

        for m_type in ['min', 'max']:
            if m_type not in finished:
                self.handler.submit_again(m_type)

        self.sample.retried += 1

    def finished_jobs(self):
        finished = []
        for m_type in ['min', 'max']:
            if self.handler.fetch_type_is_done(m_type):
                finished.append(m_type)

        return finished

    def output_summary(self):
        print('%i - %s - %s - [%s]' % (
            self.sample.id,
            self.sample.digest[0:5],
            self.current_status,
            self.sample.category))
