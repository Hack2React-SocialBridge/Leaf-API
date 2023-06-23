from leaf.models.user import PermissionsType
from tests.factories.users import UserFactory


def check_user_permissions_test():
    user = UserFactory.create(permissions=5)
    assert user.check_permissions(1) is True
    assert user.check_permissions(4) is True
    assert user.check_permissions(2) is False


def user_permissions_property_test():
    user = UserFactory.create(
        permissions=PermissionsType.read_users.value
        + PermissionsType.grant_permissions.value,
    )
    assert user.mapped_permissions == {
        "read_users": True,
        "modify_users": False,
        "grant_permissions": True,
        "revoke_permissions": False,
        "read_threats": False,
        "modify_threats": False,
    }
