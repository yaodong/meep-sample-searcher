from app.db import session
from app.sample import Sample
from sqlalchemy import desc
from app import chpc
from app import params
import logging


def delete_remote_folder(name):
    logging.info('delete %s' % name)
    chpc.remote_cmd('rm -rf %s/%s' % (params.CHPC_WORK_DIR, name))


def clean():
    folders = chpc.remote_cmd('ls %s/' % params.CHPC_WORK_DIR)

    for folder in folders.split("\n"):
        sample = session.query(Sample).filter_by(digest=folder).first()

        if not sample:
            delete_remote_folder(folder)
        elif sample.has_done == 1:
            if not is_top_one(sample):
                delete_remote_folder(folder)


def is_top_one(sample):
    top_10 = session.query(Sample) \
        .filter_by(category=sample.category, group=sample.group, status='done') \
        .order_by(desc(Sample.rating)).limit(3)
    id_list = [s.id for s in top_10]

    return sample.id in id_list
