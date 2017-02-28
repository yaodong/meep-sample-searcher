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

    category = Column(String)  # width x length x sub-class

    has_done = Column(Boolean, default=0)
    retried = Column(Integer, default=0)

    status = Column(String)
    rating = Column(Float, default=0)
    depth = Column(Float, default=0)
    loss_min = Column(Float)
    loss_max = Column(Float)

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

    def rate(self):
        if not self.loss_max or not self.loss_min:
            return False

        self.depth = (self.loss_max - self.loss_min) / (self.loss_max + self.loss_min) * 100

        loss_min_target = 0.05

        if self.loss_min < loss_min_target:
            g = 0
        else:
            g = ((loss_min_target - self.loss_min) / loss_min_target) ** 2

        self.rating = ((self.loss_max - self.loss_min) / self.loss_max) ** 2 - g

        return True
