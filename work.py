from app import endless_loop
from app.handlers.simple import Simple
from app import utils
from app import clean
import logging

logging.basicConfig(level=logging.INFO)

current_running_configs = [
    ('right-angle-30x30', 10, 30)
]

handler = Simple
category = 'right-angle-30x30'
fill_limit = 10
run_size = 10

loop_count = -1


def main():
    global loop_count

    loop_count += 1

    # if loop_count % 5 == 0:
    #     logging.info('check shortage %s' % category)
    #     if fill_limit > 0:
    #         utils.fill_shortage(category, fill_limit)

    logging.info("fetch up to %i samples" % run_size)
    for sample in utils.fetch_running_samples(category, run_size):
        logging.info('working on %i' % sample.id)
        handler(sample).work()

    logging.info('cleaning ...')
    # clean.clean()
    logging.info('cleaning done')


if __name__ == '__main__':
    endless_loop(main, 60)
