from app import endless_loop
from app.handlers.maxmin import MaxMin
from app.handlers.polarizer import Polarizer
from app import utils
from app import clean
import logging

logging.basicConfig(level=logging.INFO)

handlers = {
    'maxmin': MaxMin,
    'polarizer': Polarizer,
}

current_running_configs = [
    #('maxmin', '30x60_feb', 0, 10)
    ('polarizer', '20x20_june', 10, 10)
]

loop_count = -1


def main():
    global loop_count

    loop_count += 1

    for category, group, fill_limit, max_running_limit in current_running_configs:
        if loop_count % 5 == 0:
            logging.info('check shortage %s' % category)
            if fill_limit > 0:
                utils.fill_shortage(category, group, fill_limit)

        logging.info("fetch up to %i samples" % max_running_limit)
        for sample in utils.fetch_running_samples(category, group, max_running_limit):
            logging.info('working on %i' % sample.id)
            handler_class = handlers[category]
            handler_class(sample).work()

    logging.info('cleaning ...')
    clean.clean()
    logging.info('cleaning done')



if __name__ == '__main__':
    endless_loop(main, 60)
