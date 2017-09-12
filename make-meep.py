from app.sample import Sample
from app.db import session
from app.handlers import maxmin

samples = [69136, 105250, 105290]

for i in samples:
    s = session.query(Sample).filter_by(id=i).first()
    handler = maxmin.MaxMin(s)
    handler.make_files()

