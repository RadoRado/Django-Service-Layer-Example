import factory

from common.test_utils import fake
from common.factories import ServiceFactoryMixin

from users.services import create_user
from users.models import BaseUser


class BaseUserFactory(ServiceFactoryMixin, factory.DjangoModelFactory):
    email = factory.LazyAttribute(lambda _: fake.email())
    password = fake.password()

    class Meta:
        model = BaseUser

    @classmethod
    def get_service(cls):
        return create_user
