from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://pi@10.0.1.11/meep')

Base = declarative_base()
SessionBinding = sessionmaker(bind=engine)
session = SessionBinding()
