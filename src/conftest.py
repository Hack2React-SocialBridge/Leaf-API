import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from leaf.main import app
from inbin_backend.database import Base, get_db
from tests.test_database import SQLALCHEMY_TESTING_DATABASE_URL, engine
from inbin_backend.factories.common import Session


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    if not database_exists(SQLALCHEMY_TESTING_DATABASE_URL):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="session")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

    yield db

    db.rollback()
    connection.close()


#
@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def factory_boy_session(db_engine):

    Session.configure(bind=engine)