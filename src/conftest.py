from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import DDL, text
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from leaf.config.database import Base
from leaf.dependencies import get_db
from leaf.main import app
from tests.database_test import SQLALCHEMY_TESTING_DATABASE_URL, engine
from tests.factories.common import FactoriesSession


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    if not database_exists(SQLALCHEMY_TESTING_DATABASE_URL):
        create_database(engine.url)
    with engine.connect() as connection:
        create_extension = text(
            f"CREATE EXTENSION postgis;",
        )
        connection.execute(create_extension)
        connection.commit()
    Base.metadata.create_all(bind=engine)

    yield engine

    drop_database(engine.url)


@pytest.fixture(scope="session")
def db(db_engine):
    connection = db_engine.connect()
    db = Session(bind=connection)

    yield db

    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def factory_boy_session(db_engine):
    FactoriesSession.bind = db_engine
