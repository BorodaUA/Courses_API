import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def create_session_and_engine(db_uri):
    engine = create_engine(
        db_uri
    )
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
    )
    return {'session': session, 'engine': engine}


def create_db_file(db_name):
    sqlite3.connect(db_name)
