from app import endless_loop, utils, clean
from app.workflows.dopant import Dopant
import logging

logging.basicConfig(level=logging.INFO)

category = 'dopant'
group = '30x30'
limit = 10
max_running_limit = 10


def main():
    running_count = utils.count_running_samples(category, group)
    if running_count < max_running_limit:
        parent = utils.select_parent(category, group)
        utils.create_samples()


    for sample in utils.fetch_running_samples(category, group, max_running_limit):
        logging.info('working on %i' % sample.id)
        Dopant(sample).work()

    logging.info('cleaning ...')
    clean.clean()
    logging.info('cleaning done')


if __name__ == '__main__':
    endless_loop(main, 60)
