import matplotlib
from app.sample import Sample
from app.db import session

group = '30x30_nov'

multiple = 1

samples = session.query(Sample).filter(Sample.parent_id==0).filter_by(group=group).order_by('id').all()

sample_count = len(samples)

matplotlib.use('Agg')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Air Defects (%)")
plt.ylabel("Modulation depth% (a.u.)")
ax = fig.add_subplot(1, 1, 1)

for s in samples:
    if s.defect % 10 == 0:
        print([s.defect, s.results['depth']])
        ax.scatter(s.defect, s.results['depth'], c='g', s=4)

plt.ylim(-10, 100)

fig.savefig('%s_depth.png' % group, dpi=200)
