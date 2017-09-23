import matplotlib
from app.sample import Sample
from app.db import session

category = 'dopant'
group = '30x30'

multiple = 1

samples = session.query(Sample).filter(Sample.parent_id==0).filter_by(category=category).filter_by(group=group).filter(Sample.id>=115421).filter(Sample.id<=115528).order_by('id').all()

sample_count = len(samples)

matplotlib.use('Agg')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Air Defects (%)")
plt.ylabel("Loss Min")
ax = fig.add_subplot(1, 1, 1)

for s in samples:
    if s.defect % 10 == 0:
        ax.scatter(s.defect, s.results['loss_max'], c='r', s=4, marker='^')
        ax.scatter(s.defect, s.results['loss_min'], c='g', s=4)

#plt.ylim(-10, 100)

fig.savefig('%s_loss.png' % group, dpi=200)
