import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import SERVICE_URL, DB_CONN_STR
from tests.db_utils import clear_db


@pytest.fixture(scope="session")
def service_url():
    """
    The base URL for the service being tested
    """
    return SERVICE_URL


@pytest.fixture(scope="session")
def db_engine():
    """
    The SQLAlchemy engine used for the test session
    """
    return create_engine(DB_CONN_STR)


@pytest.fixture
def db(db_engine):
    """
    An automatically disposed SQLAlchemy DB session to be used per test case.

    All data will be cleared from the DB during disposal, so no test data will
    persist between test cases.
    """
    session = sessionmaker(bind=db_engine)()
    yield session
    try:
        clear_db(session)
        db_engine.dispose()
    except:
        pass  # terrible practice, never do this for real ;)
