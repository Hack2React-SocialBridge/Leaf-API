from sqlalchemy.orm import Session

from leaf.auth import get_current_user
from leaf.main import app
from leaf.models import User
from leaf.repositories.users import get_user_by_email


def force_authenticate(db: Session, user: User):
    app.dependency_overrides[get_current_user] = lambda: get_user_by_email(
        db,
        user.email,
    )
