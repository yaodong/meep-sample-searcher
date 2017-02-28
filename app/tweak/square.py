import random
import numpy

TWEAK_PROB = 0.1


def tweak(points, cfg):
    part_length = cfg['length']['size']
    part_width = cfg['width']['size']

    layout = numpy.array(points).reshape((part_width, part_length))

    tweak_size = cfg['tweak_size']

    tweak_length_size = random.randint(*tweak_size['length'])
    tweak_width_size = random.randint(*tweak_size['width'])

    tweak_start_length = random.randint(0, part_length - tweak_length_size)
    tweak_start_width = random.randint(0, part_width - tweak_width_size)

    tweak_end_length = tweak_start_length + tweak_length_size
    tweak_end_width = tweak_start_width + tweak_width_size

    for width_offset in range(tweak_start_width, tweak_end_width):
        for length_offset in range(tweak_start_length, tweak_end_length):
            if random.random() < TWEAK_PROB:
                tweak_to = layout[width_offset][length_offset]
                if tweak_to == 1:
                    tweak_to = 0
                else:
                    tweak_to = 1
                layout[width_offset][length_offset] = tweak_to

    return layout.flatten().tolist()
