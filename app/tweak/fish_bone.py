import random
import numpy


def tweak_more_defect(points, cfg):
    return _tweak(points, cfg, prefer_tweak_to=0)


def tweak_more_solid(points, cfg):
    return _tweak(points, cfg, prefer_tweak_to=1)


def _tweak(base_points, cfg, prefer_tweak_to):
    width = cfg['width']['size']
    length = cfg['length']['size']

    tweak_area = pick_random_tweak_area(width, length)
    base_layout = numpy.array(base_points).reshape((width, length))

    tweaked_points = []
    tweak_defect_porb = 0.5
    tweak_point_porb = 0.5

    for width_offset in range(len(base_layout)):
        for length_offset in range(len(base_layout[width_offset])):
            original_point = base_layout[width_offset][length_offset]
            if is_in_tweak_range(tweak_area, width_offset, length_offset):
                if random.random() < tweak_defect_porb:
                    should_tweak_point = random.random() < tweak_point_porb
                    if should_tweak_point:
                        if original_point == 1:
                            tweaked_point = 0
                        else:
                            tweaked_point = 1
                        tweaked_points.append(tweaked_point)
                    else:
                        tweaked_points.append(prefer_tweak_to)
                else:
                    tweaked_points.append(original_point)
            else:
                tweaked_points.append(original_point)

    return [int(i) for i in tweaked_points]


def pick_random_tweak_area(layout_width, layout_length):
    center_solid_width = 3

    solid_top_offset = int((layout_width - center_solid_width) / 2)
    solid_bottom_offset = layout_width - solid_top_offset

    tweak_width = random.randint(3, 7)
    tweak_length = random.randint(3, 10)

    tweak_width_range = pick_tweak_width_range(layout_width, solid_top_offset, solid_bottom_offset, tweak_width)
    tweak_length_range = pick_tweak_length_range(layout_length, tweak_length)

    tweak_area = {
        'width': {
            'min': tweak_width_range[0],
            'max': tweak_width_range[1]
        },
        'length': {
            'min': tweak_length_range[0],
            'max': tweak_length_range[1]
        }
    }

    return tweak_area


def pick_tweak_width_range(layout_width, solid_top_offset, solid_bottom_offset, tweak_width):
    if random.random() > 0.5:
        offset = (0, solid_top_offset - tweak_width)
    else:
        offset = (solid_bottom_offset, layout_width - tweak_width)

    offset = random.randint(*offset)
    return [offset, offset + tweak_width]


def pick_tweak_length_range(layout_length, tweak_length):
    tweak_length_offset = random.randint(0, layout_length - tweak_length)
    return [tweak_length_offset, tweak_length_offset + tweak_length]


def is_in_tweak_range(area, width_offset, length_offset):
    if width_offset < area['width']['min']:
        return False

    if width_offset > area['width']['max']:
        return False

    if length_offset < area['length']['min']:
        return False

    if length_offset > area['length']['max']:
        return False

    return True
