from app.db import session
from app.handlers.maxmin import MaxMin
from app.handlers.polarizer import Polarizer


class Worker:
    STATE_READY = 'ready'
    STATE_SUBMITTED = 'submitted'
    STATE_RATING = 'rating'
    STATE_DONE = 'done'
    STATE_ERROR = 'error'

    def __init__(self, sample):
        self.sample = sample

        if sample.status is None:
            sample.status = self.STATE_READY

        self.handler = self.make_handler(self.sample)

    def work(self):
        status = self.sample.status
        handler = self.handler

        if status == self.STATE_READY:
            handler.submit()
        elif status == self.STATE_SUBMITTED:
            try:
                handler.pull()
            except handler.StillRunning:
                pass
            except handler.Interrupted:
                handler.resume()
            except handler.FatalError:
                handler.abandon()

        elif status == self.STATE_ERROR:
            pass
        else:
            raise RuntimeError('unkown status')

        session.add(self.sample)
        session.commit()

    @staticmethod
    def make_handler(sample):
        if sample.category == 'maxmin':
            handler = MaxMin(sample)
        elif sample.category == 'polarizer':
            handler = Polarizer(sample)
        else:
            raise RuntimeError('unknown category %s' % sample.category)

        return handler

        # @property
        # def current_status(self):
        #     return self.sample.status
        #
        # @current_status.setter
        # def current_status(self, value):
        #     self.sample.status = value
        #
        # def work(self):
        #     self.output_summary()
        #
        #     action = getattr(self, 'when_' + self.current_status)
        #     action()
        #     session.add(self.sample)
        #     session.commit()
        #
        # def when_ready(self):
        #     print('generating files')
        #     self.handler.make_program_files()
        #
        #     print('uploading files')
        #     self.handler.upload_program_files()
        #
        #     print('submitting task')
        #     self.handler.submit_all()
        #     self.current_status = self.STATE_SUBMITTED
        #
        # def when_submitted(self):
        #     print('checking job status')
        #     jobs = self.handler.fetch_jobs()
        #     if len(jobs) > 0:
        #         self.describe_jobs(jobs)
        #     else:
        #         finished = self.finished_jobs()
        #         print('meep finished: %s' % ', '.join(finished))
        #         if len(finished) == 2:
        #             self.current_status = self.STATE_RATING
        #         else:
        #             print('re-making')
        #             self.handler.make_program_files()
        #             print('re-uploading')
        #             self.handler.upload_program_files()
        #             print('re-starting')
        #             self.restart_failed_jobs(finished)
        #
        # def when_rating(self):
        #     print('calling matlab')
        #     self.handler.call_matlab()
        #
        #     for m_type in ['min', 'max']:
        #         loss = self.handler.fetch_matlab_result(m_type)
        #         setattr(self.sample, 'loss_%s' % m_type, loss)
        #
        #     if not self.sample.rate():
        #         self.current_status = self.STATE_ERROR
        #         self.sample.has_done = 1
        #         print('error')
        #     else:
        #         self.current_status = self.STATE_DONE
        #         self.sample.has_done = 1
        #         print('done')
        #         self.handler.clean()
        #
        # def when_error(self):
        #     self.sample.has_done = 1
        #
        # @staticmethod
        # def describe_jobs(jobs):
        #     for job in jobs:
        #         if job['state'] == 'PD':
        #             print('job %s %s [PD], expect start at %s' % (job['job_id'], job['job_name'], job['time_expect']))
        #         else:
        #             print('job %s %s [%s], time used %s' % (job['job_id'], job['job_name'], job['state'], job['time_used']))
        #
        # def restart_failed_jobs(self, finished):
        #     if self.sample.retried > 3:
        #         self.current_status = self.STATE_ERROR
        #         return
        #
        #     for m_type in ['min', 'max']:
        #         if m_type not in finished:
        #             self.handler.submit_again(m_type)
        #
        #     self.sample.retried += 1
        #
        # def finished_jobs(self):
        #     finished = []
        #     for m_type in ['min', 'max']:
        #         if self.handler.fetch_type_is_done(m_type):
        #             finished.append(m_type)
        #
        #     return finished
        #
        # def output_summary(self):
        #     print('%i - %s - %s - [%s]' % (
        #         self.sample.id,
        #         self.sample.digest[0:5],
        #         self.current_status,
        #         self.sample.category))
