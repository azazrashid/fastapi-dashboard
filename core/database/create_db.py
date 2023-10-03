from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database
from core.config import config


def validate_database():
    """
    Validate the existence of a database specified in the DATABASE_URL
    configuration.

    If the database does not exist, it will create a new one.
    """
    engine = create_engine(config.DATABASE_URL)

    # Check if the database already exists
    if database_exists(engine.url):
        print("Database already exists")
    else:
        # Create a new database
        create_database(engine.url)
        print("New database created")
