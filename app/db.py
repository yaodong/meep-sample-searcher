from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path


db_file = path.join(path.dirname(__file__), '..', 'sqlite3.db')
engine = create_engine('postgresql://pi@10.0.1.9/meep')

Base = declarative_base()
SessionBinding = sessionmaker(bind=engine)
session = SessionBinding()
