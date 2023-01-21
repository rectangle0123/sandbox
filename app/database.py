from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sandbox.sqlite3', echo=False)
Base = declarative_base()
