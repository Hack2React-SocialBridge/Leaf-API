from unittest.mock import patch

from tests.factories.users import UserFactory
from leaf.auth import verify_token, generate_confirmation_token
from leaf.repositories.users import get_user_by_email


def test_token_generation(client):
    user = UserFactory.create()
    r = client.post(
        "users/token/", json={"username": user.email, "password": "Elektryk1@"}
    )
    assert r.status_code == 200
    assert verify_token(r.json()["access_token"]) == user.email


def test_register_new_user(db, client):
    with patch("leaf.routers.users.send_mail") as send_mail_mock:
        test_user_email = "register_test@example.it"
        r = client.post(
            "users/register/", json={
                "email": test_user_email,
                "password": "Elektryk1@",
                "first_name": "Test",
                "last_name": "Test",
            }
        )
        db_user = get_user_by_email(db, test_user_email)
        send_mail_mock.delay.assert_called()
        assert r.status_code == 201
        assert db_user.email == test_user_email


def test_confirm_user_passed(db, client):
    user = UserFactory.create(disabled=True)
    token = generate_confirmation_token(user.email)
    r = client.post("users/confirm", json={"key": token})
    db_user = get_user_by_email(db, user.email)
    assert r.status_code == 200
    assert db_user.disabled is False


def test_confirm_user_not_passed(db, client):
    user = UserFactory.create(disabled=True)
    token = "invalid_token"
    r = client.post("users/confirm", json={"key": token})
    db_user = get_user_by_email(db, user.email)
    assert r.status_code == 400
    assert r.json() == {"detail": "Invalid token"}
    assert db_user.disabled is True
