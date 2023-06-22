from __future__ import annotations

from leaf.models import User
from leaf.repositories.users import (
    create_one,
    get_active_user_by_email,
    get_user_by_email,
    update_one,
)
from tests.factories.users import UserFactory


def test_get_user_by_email(db):
    user = UserFactory.create()
    db_user = get_user_by_email(db, user.email)
    assert isinstance(db_user, User)
    assert db_user.id == user.id


def test_get_active_user_by_email_passed_case(db):
    user = UserFactory.create(disabled=False)
    db_user = get_active_user_by_email(db, user.email)
    assert isinstance(db_user, User)
    assert db_user.id == user.id


def test_get_active_user_by_email_not_passed_case(db):
    user = UserFactory.create(disabled=True)
    db_user = get_active_user_by_email(db, user.email)
    assert db_user is None


def test_create_one(db):
    create_one(
        db,
        email="create_one_test@test.com",
        hashed_password="test",
        first_name="test",
        last_name="test",
        disabled=True,
    )
    db_user = get_user_by_email(db, email="create_one_test@test.com")
    assert db_user is not None


def test_update_one(db):
    user = UserFactory.create(first_name="before_update")
    update_one(db, user.email, first_name="after_update")
    db_user = get_user_by_email(db, user.email)
    assert db_user.first_name == "after_update"
