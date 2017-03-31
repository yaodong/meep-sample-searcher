from app.sample import Sample
from app.db import session
from app.utils import draw_sample
import random

width = 30
length = 60
category = '30x60_feb'
size = width * length

for defect in range(10, 100, 5):
    for repeat in range(10):
        points = []
        defect_points = int(size * defect / 100)
        solid_points = size - defect_points

        for _ in range(defect_points):
            points.append(0)

        for _ in range(solid_points):
            points.append(1)

        for _ in range(50):
            random.shuffle(points)

        s = Sample()
        s.category = category
        s.parent_id = 0
        s.parts = {'main': points}
        s.update_digest()

        session.add(s)
        session.commit()
