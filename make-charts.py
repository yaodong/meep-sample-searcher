import matplotlib
from app.sample import Sample
from app.db import session

category = '30x30_nov'

multiple = 1

samples = session.query(Sample).filter_by(category=category).order_by('id').all()

sample_count = len(samples)

matplotlib.use('Qt5Agg')

start_id = 41065

import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.depth > 60 and s.id >= start_id:
        i += 1
        ax.scatter(i, s.loss_min * multiple, c='r')
        ax.scatter(i, s.loss_max * multiple, c='g')

fig.savefig('%s_loss.png' % category, dpi=200)

# ====

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.depth > 60 and s.id >= start_id:
        i += 1
        ax.scatter(i, s.loss_min * multiple, c='r')

fig.savefig('%s_loss_min.png' % category, dpi=200)

# ====

fig = plt.figure()
plt.xlabel("Sequence")
plt.ylabel("Loss (a.u.)")
ax = fig.add_subplot(1, 1, 1)

i = 0
for s in samples:
    if s.depth > 60 and s.id >= start_id:
        i += 1
        ax.scatter(i, s.loss_max * multiple, c='g')

fig.savefig('%s_loss_max.png' % category, dpi=200)
