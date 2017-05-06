from app import endless_loop
from app.handlers.maxmin import MaxMin
from app.handlers.polarizer import Polarizer
from app import utils
from app import clean
import logging

logging.basicConfig(level=logging.DEBUG)

handlers = {
    'maxmin': MaxMin,
    'polarizer': Polarizer,
}

current_running_configs = [
    ('polarizer', '20x20', 0)
]

loop_count = -1


def main():
    global loop_count

    loop_count += 1

    logging.info('cleaning ...')
    # clean.clean()
    logging.info('cleaning done')

    for category, group, max_running_limit in current_running_configs:
        if loop_count % 5 == 0:
            logging.info('check shortage %s' % category)
            utils.fill_shortage(category, group, max_running_limit)

        for sample in utils.fetch_running_samples(category, group, 100):
            logging.info('working on %i' % sample.id)
            handler_class = handlers[category]
            handler_class(sample).work()


if __name__ == '__main__':
    endless_loop(main, 60)
