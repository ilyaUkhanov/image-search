
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# FORMAT LIKE sqlite+pysqlite:///path/to/database.db'
SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_CONNECTION_STRING', 'sqlite+pysqlite:///:memory:')

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_size=100, pool_recycle=3600)

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

class DatabaseService:
    def session_factory():
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        return _SessionFactory()
