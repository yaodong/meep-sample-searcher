from app import db
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import JSON
from hashlib import md5
import numpy
from math import exp


class Sample(db.Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    defect = Column(Integer)

    category = Column(String)
    group = Column(String)  # width x length x sub-class

    has_done = Column(Boolean, default=0)
    retried = Column(Integer, default=0)

    status = Column(String)
    rating = Column(Float, default=0)

    results = Column(JSON)

    digest = Column(String)

    parts = Column(JSON)

    def update_digest(self):
        points = []
        for k, v in sorted(self.parts.items()):
            points.extend(v)

        self.digest = md5(','.join(str(p) for p in points).encode('utf-8')).hexdigest()

        defects = 0
        for p in points:
            if p == 0:
                defects += 1

        self.defect = defects / len(points) * 100
