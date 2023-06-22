from __future__ import annotations

from sqlalchemy import update
from sqlalchemy.orm import Session

from leaf.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_active_user_by_email(db: Session, email: str) -> User | None:
    user = (
        db.query(User)
        .filter(
            User.disabled == False,
            User.email == email,
        )
        .first()
    )
    return user


def create_one(db: Session, **user_props) -> User:
    db_user = User(**user_props)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_one(db: Session, user_email: str, **user_props) -> User | None:
    db.execute(
        update(User)
        .where(
            User.email == user_email,
        )
        .values(**user_props),
    )
    db.commit()
    return get_user_by_email(db, user_email)
