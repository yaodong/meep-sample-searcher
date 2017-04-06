from app.db import session
from app import params
from app.handlers.maxmin import MaxMin
# from app.params import CATEGORIES
from app.sample import Sample
from sqlalchemy import desc
from numpy import random
import numpy
from app import tweak


def fill_shortage(category, group, limit):
    count_not_done = count_running_samples(category, group)
    if count_not_done >= limit:
        return

    print('fill category %s:%s' % (category, group))

    shortage = limit - count_not_done
    for _ in range(shortage):
        create_samples_by_editor(category, group)


def count_running_samples(category, group):
    return session.query(Sample).filter_by(category=category, group=group, has_done=0).count()


def fetch_running_samples(category, group, max_limit):
    return session.query(Sample).filter_by(category=category, group=group, has_done=0).order_by('id').limit(max_limit).all()


def select_parent(category, group):
    samples = session.query(Sample).filter_by(
        has_done=1,
        status='done',
        category=category,
        group=group,
    ).order_by(desc(Sample.rating)).limit(10).all()

    if not samples:
        return None

    if len(samples) < 10:
        selected = samples[0]
    else:
        relative_probabilities = [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
        selected_offset = random.choice(range(0, len(samples)), p=relative_probabilities)
        selected = samples[selected_offset]

    return selected


def create_samples_by_editor(category, group):
    parent = select_parent(category, group)

    if not parent:
        print('no seed found for %s' % category)
        return

    # parts = create_parts(parent)

    parts = MaxMin(parent).create_parts(parent)

    sample = Sample()
    sample.parent_id = parent.id
    sample.category = parent.category
    sample.group = parent.group
    sample.defect = 0
    sample.parts = parts
    sample.update_digest()

    if not digest_exists(sample.digest):
        session.add(sample)
        session.commit()



def digest_exists(digest):
    return session.query(Sample).filter_by(digest=digest).first() is not None


def draw_sample(sample):
    cfg = CATEGORIES[sample.category]
    base_width = cfg['width']
    base_length = cfg['length']

    layout = []
    for i in range(base_width):
        layout.extend([' ' for _ in range(base_length)])

    layout = numpy.array(layout).reshape(base_width, base_length)

    for part_name, part_cfg in cfg['parts'].items():
        w_offset = part_cfg['width']['offset']
        w_size = part_cfg['width']['size']

        l_offset = part_cfg['length']['offset']
        l_size = part_cfg['length']['size']

        part_layout = numpy.array(sample.parts[part_name]).reshape(w_size, l_size)

        for part_row_number in range(w_size):
            for part_column_number in range(l_size):
                global_w_offset = w_offset + part_row_number
                global_l_offset = l_offset + part_column_number
                layout[global_w_offset][global_l_offset] = part_layout[part_row_number][part_column_number]

    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if str(layout[i][j]) == '1':
                print(' ■', end='')
            else:
                print('  ', end='')

        print('')
