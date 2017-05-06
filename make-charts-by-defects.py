import matplotlib
from app.sample import Sample
from app.db import session

category = 'polarizer'
group = '20x20'

multiple = 1
min_id = 89608
max_id = 89787

samples = session.query(Sample).filter_by(category=category, group=group).filter(Sample.id >= min_id).filter(Sample.id <= max_id).order_by('id').all()
sample_count = len(samples)

# matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

fig = plt.figure()
plt.xlabel("Defect %")
plt.ylabel("Result (*10^5)")
ax = fig.add_subplot(1, 1, 1)

for s in samples:
  ax.scatter(s.defect, s.rating, c='b')

fig.savefig('%s_result_by_defect.png' % category, dpi=200)
