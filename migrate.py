from app.db import session
from app.sample import Sample

keys = set()

i = 1
for sample in session.query(Sample).order_by('id').all():

    i += 1

    data = sample.data

    main = data['parts']['main']
    if not isinstance(main, list):
        main = main['points']

    new_data = {
        'main': main,
    }

    sample.data = new_data

    keys.add(sample.digest)

    session.add(sample)
    if i % 2000 == 0:
        session.commit()

    print(sample.id)

session.commit()
