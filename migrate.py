from app.db import session
from app.sample import Sample


i = 1
for sample in session.query(Sample).order_by('id').all():

    i += 1

    # edit here

    session.add(sample)
    if i % 2000 == 0:
        print(i)
        session.commit()


session.commit()
