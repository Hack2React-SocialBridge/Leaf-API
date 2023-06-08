from tests.factories.users import UserFactory
from leaf.auth import verify_token


def test_token_generation(client):
    user = UserFactory.create()
    r = client.post(
        "users/token/", json={"username": user.email, "password": "Elektryk1@"}
    )
    assert r.status_code == 200
    assert verify_token(r.json()["access_token"]) == user.email
