from sqlalchemy.orm import Session

from leaf.models import User


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def create_one(db: Session, **user_props) -> User:
    db_user = User(**user_props)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
