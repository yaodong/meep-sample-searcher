from app import endless_loop
from app import utils
from app import clean
from app.state_machine import StateMachine

instance_limit = {
    # '30x30w4': 0,
    '20x30r': 0,
    '20x60r': 0,
    #'30x60': 20,
    '30x30_nov': 50,
}

loop_count = -1


def main():
    global loop_count

    loop_count += 1

    print('loop %i' % loop_count)
    print('-' * 30)

    print('cleaning ...')
    clean.clean()
    print('cleaning done')
    print('-' * 30)

    for category, limit in instance_limit.items():

        if limit > 0 and loop_count % 5 == 0:
            print('check shortage %s' % category)
            utils.fill_shortage(category, limit)
            print('-' * 30)

        for sample in utils.fetch_in_progress_samples(category):
            StateMachine(sample).work()
            print('-' * 30)


if __name__ == '__main__':
    endless_loop(main, 60)
