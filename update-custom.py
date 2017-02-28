from app.sample import Sample
from app.db import session

samples = session.query(Sample).filter_by(category='30x30_nov').all()

for s in samples:
    s.update_digest()
    s.rate()
    session.add(s)

session.commit()
