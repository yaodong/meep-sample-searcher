from time import sleep
from sys import stdout

def endless_loop(func, sleep_time=10):

    while True:
        func()
        print('\n... _(:3J∠)_ ', end='')
        for _ in range(0, sleep_time):
            print('.', end='')
            stdout.flush()
            sleep(1)
        print('\n')
