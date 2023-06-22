from __future__ import annotations

from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_TESTING_DATABASE_URL = (
    f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}"
    f"@{environ.get('POSTGRES_HOST')}:{environ.get('POSTGRES_PORT')}/test"
)

engine = create_engine(SQLALCHEMY_TESTING_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
