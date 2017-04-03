import random
import numpy

TWEAK_PROB = 0.1


def tweak(points, cfg):
    part_y_size = cfg['y']['size']
    part_z_size = cfg['z']['size']

    layout = numpy.array(points).reshape((part_z_size, part_y_size))

    if part_y_size > 15 and part_z_size > 15:
        tweak_width_size = tweak_length_size = random.randint(3, 5)
    else:
        tweak_width_size = tweak_length_size = random.randint(2, 4)

    tweak_start_length = random.randint(0, part_y_size - tweak_length_size)
    tweak_start_width = random.randint(0, part_z_size - tweak_width_size)

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
