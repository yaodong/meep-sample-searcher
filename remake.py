from app import handler
from app.db import session
from app.sample import Sample


ids = [
  '43635'
]

for i in ids:
	s = session.query(Sample).filter_by(id=i).first()
	h = handler.Handler(s)
	h.make_program_files()
	h.upload_program_files()
	h.submit_all()
	print(s.digest)
