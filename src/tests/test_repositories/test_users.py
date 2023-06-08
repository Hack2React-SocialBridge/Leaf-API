from leaf.repositories.users import get_user_by_email, create_one
from tests.factories.users import UserFactory
from leaf.models import User


def test_get_user_by_email(db):
    user = UserFactory.create()
    db_user = get_user_by_email(db, user.email)
    assert isinstance(db_user, User)
    assert db_user.id == user.id
