from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

import os

DB_HOST = os.getenv("DB_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))


DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, POSTGRES_PORT, POSTGRES_DB
)

engine = create_engine(DATABASE_URL, echo=True)


Base = declarative_base()


class Database:

    def __init__(self) -> None:
        self._engine = engine
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database_instance = Database()
