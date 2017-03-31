from app.utils import draw_sample
from app.db import session
from app.sample import Sample
from sqlalchemy import desc
from time import sleep


def main():
    categories = [
        #'20x60r',
        '30x60_feb',
        #'15x30'
    ]

    print('=')

    for category in categories:

        tops = session.query(Sample).filter_by(category=category, status='done').order_by(desc('depth')).limit(10).all()
        draw_sample(tops[0])
        #draw_sample(session.query(Sample).get(65757))
        print('=' * 20)
        print('current top 10 in category %s:' % category)
        print('num\tdigest\tdepth\t\tmax\t\tmin\t\tdefect')

        for s in tops:
            print('%i\t%s\t%f\t%f\t%f\t%i' % (
                s.id, s.digest[0:5], s.depth, s.loss_max, s.loss_min, s.defect))

        print('=' * 20)

while True:
    main()
    print('sleep')
    sleep(150)
