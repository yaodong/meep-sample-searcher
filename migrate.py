from app.db import session
from app.sample import Sample


i = 1
for sample in session.query(Sample).order_by('id').all():

    i += 1

    sample.results = {
        'depth': sample.depth,
        'loss_min': sample.loss_min,
        'loss_max': sample.loss_max,
    }

    session.add(sample)
    if i % 2000 == 0:
        print(i)
        session.commit()


session.commit()
