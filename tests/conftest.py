from typing import Iterator
import pytest
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from app import crud
from app.db import Base, engine_test, session_test, Session as DBSession
from app.dtos import UserForRegister


def get_db() -> Iterator[Session]:
    try:
        db = DBSession()
        yield db
    finally:
        db.close()


def init_test_db(db_session: Session) -> None:
    """Adding the initial test user to the test database"""
    Base.metadata.create_all(bind=engine_test)
    user = crud.get_by_email(db_session, email="test@example.com")
    if not user:
        user_in = UserForRegister(
            email="test@example.com", password="secret", is_superuser=True,
        )
        user = crud.create_user(db_session, user_in=user_in)


@pytest.fixture(scope="session", autouse=True)
def database():
    """Make sure all tables are dropped after all tests are run."""
    assert not database_exists(
        engine_test.url
    ), "Test database already exists. Aborting tests."
    try:
        create_database(engine_test.url)
        init_test_db(session_test)
        yield
    finally:
        drop_database(engine_test.url)


@pytest.fixture(scope="function")
def session():
    """
    Return a session that is bound to a transaction object that can be rolled back.

    Transaction is rolled back after each test function, so that test db does not
    get polluted between test cases.

    `app.dependency_overrides` sets correct db dependency for API tests.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
