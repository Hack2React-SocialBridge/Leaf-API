from __future__ import annotations

from sqlalchemy.orm import scoped_session, sessionmaker

from leaf.database import engine

FactoriesSession = scoped_session(
    sessionmaker(autoflush=False, bind=engine),
)
