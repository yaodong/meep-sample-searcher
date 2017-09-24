import random
import numpy

TWEAK_PROB = 0.1


def tweak(points, cfg):
    part_length = cfg['length']['to']
    part_width = cfg['width']['to']

    layout = numpy.array(points).reshape((part_width, part_length))

    tweak_length_size = part_length // 10
    tweak_width_size = part_width // 10

    if part_length > 15 and part_width > 15:
        tweak_width_size = tweak_length_size = random.randint(3, 5)
    else:
        tweak_width_size = tweak_length_size = random.randint(2, 4)

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
