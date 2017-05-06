import matplotlib
from app.sample import Sample
from app.db import session

category = '30x30_nov'

multiple = 1
min_id = 41065

samples = session.query(Sample).filter_by(category=category).order_by('id').all()

sample_count = len(samples)

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Defect")
plt.ylabel("Depth% (a.u.)")
ax = fig.add_subplot(1, 1, 1)

with open('sequeue.txt', 'w') as sf:
    for s in samples:
        if s.id > 41087:
            sf.write("%s\n" % (s.id - 41087))
with open('depth.txt', 'w') as sf:
    for s in samples:
        if s.id > 41087:
            sf.write("%s\n" % (s.depth))

# for s in handlers:
#     if not s.status == 'done':
#         continue
#     if s.id > 41065:
#         ax.scatter(s.id - 41065, s.depth, c='g')
#
# fig.savefig('%s_depth.png' % category, dpi=200)
