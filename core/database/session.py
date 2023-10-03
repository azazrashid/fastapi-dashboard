from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from core.config import config
from sqlmodel import create_engine, Session


database_url = config.DATABASE_URL

Base = declarative_base()


def get_connection():
    """
    Create a database connection.

    Returns:
        sqlmodel.Database: A database connection.
    """
    return create_engine(database_url, echo=False, poolclass=NullPool)


def get_session():
    """
    Get a database session.

    Yields:
        sqlmodel.Session: A database session.
    """
    with Session(get_connection()) as session:
        yield session
