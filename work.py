from app import endless_loop
from app.handlers.maxmin import MaxMin
from app.handlers.polarizer import Polarizer
from app import utils
from app import clean

handlers = {
    'maxmin': MaxMin,
    'polarizer': Polarizer,
}

current_running_configs = [
    ('maxmin', '30x60_feb', 1)
]

loop_count = -1


def main():
    global loop_count

    loop_count += 1

    # print('loop %i' % loop_count)
    # print('-' * 30)
    #
    # print('cleaning ...')
    # clean.clean()
    # print('cleaning done')
    # print('-' * 30)

    for category, group, max_running_limit in current_running_configs:

        if loop_count % 5 == 0:
            print('check shortage %s' % category)
            utils.fill_shortage(category, group, max_running_limit)
            print('-' * 30)

        for sample in utils.fetch_running_samples(category, group):
            handler_class = handlers[category]
            handler_class(sample).work()
            print('-' * 30)


if __name__ == '__main__':
    endless_loop(main, 60)
