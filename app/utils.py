from app.db import session
from app import params
from app.params import CATEGORIES
from app.sample import Sample
from sqlalchemy import desc
from numpy import random
import numpy
from app import tweak


def fill_shortage(category, limit):
    count_not_done = count_not_done_samples(category)
    if count_not_done >= limit:
        return

    print('fill category %s' % category)

    shortage = limit - count_not_done
    for _ in range(shortage):
        create_samples_by_editor(category)


def count_not_done_samples(category):
    return session.query(Sample).filter_by(category=category, has_done=0).count()


def fetch_in_progress_samples(category):
    return session.query(Sample).filter_by(category=category, has_done=0).order_by('id').all()


def select_parent(category):
    samples = session.query(Sample).filter_by(
        has_done=1,
        status='done',
        category=category
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


def create_samples_by_editor(category):
    parent = select_parent(category)

    if not parent:
        print('no seed found for %s' % category)
        return

    parts = create_parts(parent)

    sample = Sample()
    sample.parent_id = parent.id
    sample.category = parent.category
    sample.defect = 0
    sample.parts = parts
    sample.update_digest()

    if not digest_exists(sample.digest):
        session.add(sample)
        session.commit()


def create_parts(parent):
    category_params = params.CATEGORIES[parent.category]

    new_parts = {}
    for part_name, part_cfg in category_params['parts'].items():
        tweak_module = getattr(tweak, category_params['parts'][part_name]['tweak'])
        tweak_method = getattr(tweak_module, 'tweak')

        if part_name in parent.parts:
            old_part = parent.parts[part_name]
        else:
            part_width = part_cfg['width']['size']
            part_length = part_cfg['length']['size']
            old_part = [random.randint(2) for _ in range(part_width * part_length)]

        new_parts[part_name] = tweak_method(old_part, part_cfg)

    return new_parts


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
