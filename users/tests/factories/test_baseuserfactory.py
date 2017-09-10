from unittest.mock import patch

from django.test import TestCase

from users.factories import BaseUserFactory


class BaseUserFactoryTests(TestCase):
    @patch('users.factories.create_user')
    def test_creating_user_with_factory_calls_service(self, create_user_mock):
        BaseUserFactory()

        self.assertTrue(create_user_mock.called)
        self.assertEqual(1, create_user_mock.call_count)
