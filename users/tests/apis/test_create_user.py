from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from common.test_utils import fake


class CreateUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:create')

    @patch('users.apis.create_user')
    def test_service_is_called_when_data_is_valid(self, create_user_mock):
        data = {
            'email': fake.email(),
            'password': fake.password()
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(202, response.status_code)

        self.assertTrue(create_user_mock.called)
        self.assertEqual(1, create_user_mock.call_count)

        call_kwargs = create_user_mock.call_args_list[0][1]

        self.assertEqual(data, call_kwargs)
