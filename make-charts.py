import matplotlib
from app.sample import Sample
from app.db import session

category = 'maxmin'
group = '30x60_feb'

# seed 69136 - 69215
# run 69316 - 91722

multiple = 1

samples = session.query(Sample)\
                 .filter_by(group=group)\
                 .filter_by(category=category)\
                 .filter_by(status="done")\
                 .filter(Sample.id>=69316).filter(Sample.id<=91722).order_by('id').all()

sample_count = len(samples)

matplotlib.use('Agg')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.results['depth'] > 60:
        i += 1
        ax.scatter(i, s.results['loss_min'] * multiple, c='r', s=1)
        ax.scatter(i, s.results['loss_max'] * multiple, c='g', s=1)

fig.savefig('%s_loss.png' % category, dpi=200)


# ====

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.results['depth'] > 60:
        i += 1
        ax.scatter(i, s.results['loss_min'] * multiple, c='r', s=1)

fig.savefig('%s_loss_min.png' % category, dpi=200)

# ====

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.results['depth'] > 60:
        i += 1
        ax.scatter(i, s.results['loss_max'] * multiple, c='g', s=1)

fig.savefig('%s_loss_max.png' % category, dpi=200)
