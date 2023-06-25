from __future__ import annotations

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from leaf.auth import (
    confirm_token,
    generate_confirmation_token,
    verify_password,
    verify_token,
)
from leaf.config.config import get_settings
from leaf.models import User
from leaf.repositories.users import get_user_by_email
from tests.factories.users import UserFactory

settings = get_settings()


def test_token_generation(client: TestClient):
    user = UserFactory.create()
    r = client.post(
        "users/token/",
        json={"username": user.email, "password": "Elektryk1@"},
    )
    assert r.status_code == 200
    assert (
        verify_token(
            r.json()["access_token"],
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        == user.email
    )


def test_register_new_user(db: Session, client: TestClient):
    with patch("leaf.routers.users.send_mail") as send_mail_mock:
        test_user_email = "register_test@example.it"
        r = client.post(
            "users/register/",
            json={
                "email": test_user_email,
                "password": "Elektryk1@",
                "first_name": "Test",
                "last_name": "Test",
            },
        )
        db_user = get_user_by_email(db, test_user_email)
        send_mail_mock.delay.assert_called()
        assert r.status_code == 201
        assert db_user.email == test_user_email


def test_confirm_user_passed(db: Session, client: TestClient):
    user = UserFactory.create(disabled=True)
    token = generate_confirmation_token(
        user.email,
        secret_key=settings.SECRET_KEY,
        security_password_salt=settings.SECURITY_PASSWORD_SALT,
    )
    r = client.post("users/confirm", json={"key": token})
    db_user = get_user_by_email(db, user.email)
    assert r.status_code == 200
    assert db_user.disabled is False


def test_confirm_user_not_passed(db: Session, client: TestClient):
    user = UserFactory.create(disabled=True)
    token = "invalid_token"
    r = client.post("users/confirm", json={"key": token})
    db_user = get_user_by_email(db, user.email)
    assert r.status_code == 400
    assert r.json() == {"detail": "Invalid token"}
    assert db_user.disabled is True


@patch("leaf.routers.users.send_mail")
@patch("jinja2.Template.render")
def test_password_reset_view_as_active_user(
    render_mock: MagicMock,
    send_mail_mock: MagicMock,
    client: TestClient,
):
    render_mock.return_value = "test"
    test_user_email = "password_reset_view@example.it"
    UserFactory.create(email=test_user_email)
    r = client.post(
        "users/password-reset",
        json={"email": test_user_email},
    )
    rendered_token = render_mock.call_args_list[0].kwargs["confirmation_token"]
    assert r.status_code == 200
    assert (
        confirm_token(
            rendered_token,
            settings.SECRET_KEY,
            settings.SECURITY_PASSWORD_SALT,
        )
        == test_user_email
    )
    assert r.json() == {
        "detail": "Password reset instructions have been sent to the provided email address.",
    }
    send_mail_mock.delay.assert_called()


@patch("leaf.routers.users.send_mail")
def test_password_reset_view_as_inactive_user(
    send_mail_mock: MagicMock,
    client: TestClient,
):
    test_user_email = "password_reset_view_inactive@example.it"
    UserFactory.create(email=test_user_email, disabled=True)
    r = client.post(
        "users/password-reset",
        json={"email": test_user_email},
    )
    assert r.status_code == 200
    assert r.json() == {
        "detail": "Password reset instructions have been sent to the provided email address.",
    }
    send_mail_mock.assert_not_called()


def test_password_reset_confirm_view_passed(db: Session, client: TestClient):
    user = UserFactory.create()
    new_password = "password_after_reset"
    r = client.post(
        "users/password-reset-confirm",
        json={
            "key": generate_confirmation_token(
                user.email,
                settings.SECRET_KEY,
                settings.SECURITY_PASSWORD_SALT,
            ),
            "new_password": new_password,
        },
    )
    db_user = db.query(User).filter(User.email == user.email).first()
    assert r.status_code == 200
    assert verify_password(new_password, db_user.hashed_password)


def test_password_reset_confirm_view_not_passed(
    db: Session,
    client: TestClient,
):
    user = UserFactory.create()
    new_password = "password_after_reset"
    r = client.post(
        "users/password-reset-confirm",
        json={"key": "invalid_token", "new_password": new_password},
    )
    db_user = db.query(User).filter(User.email == user.email).first()
    assert r.status_code == 400
    assert r.json() == {"detail": "Invalid token"}
    assert not verify_password(new_password, db_user.hashed_password)
