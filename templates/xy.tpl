import re

file = "run-max.log"

x_values = []
y_values = []
for segment in re.findall('block, center = \(([-0-9\.,]+)\)', open(file).read()):
	three = segment.split(',')
	x_values.append(three[0])
	y_values.append(three[1])

open('x_values.txt', 'w').write('\n'.join(x_values) + '\n')
open('y_values.txt', 'w').write('\n'.join(y_values) + '\n')
