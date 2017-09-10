from django.test import TestCase

from users.services import create_user
from users.models import BaseUser

from common.test_utils import fake


class CreateUserTests(TestCase):
    def test_creating_user_with_proper_data_is_working(self):
        self.assertEqual(0, BaseUser.objects.count())

        user_data = {
            'email': fake.email(),
            'password': fake.password()
        }

        create_user(**user_data)

        self.assertEqual(1, BaseUser.objects.count())
        self.assertTrue(
            BaseUser.objects.filter(email=user_data['email']).exists()
        )
