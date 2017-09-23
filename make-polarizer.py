from app.sample import Sample
from app.db import session
from random import randint
from hashlib import md5

width = 20
length = 20
category = 'polarizer-30x30'
size = width * length

count = 290

for i in range(count):
    points = []
    for j in range(width * length):
        points.append(randint(0, 250) * 2)

    s = Sample()
    s.category = category
    s.parent_id = 0
    s.parts = points
    s.digest = md5(','.join(str(p) for p in points).encode('utf-8')).hexdigest()

    session.add(s)
    session.commit()
