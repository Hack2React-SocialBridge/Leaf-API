import factory
from leaf.models import User
from leaf.routers.users import get_password_hash
from tests.factories.common import FactoriesSession


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = FactoriesSession
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"user{n}@example.it")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("Elektryk1@"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    disabled = False
