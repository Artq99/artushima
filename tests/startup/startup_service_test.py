"""
The testing module for the startup service.
"""

from unittest import TestCase
from unittest.mock import create_autospec

from artushima.startup import startup_service
from artushima.user import user_service


class SuperuserExistsTest(TestCase):

    def setUp(self):
        self.user_service_mock = create_autospec(user_service)
        startup_service.user_service = self.user_service_mock

    def tearDown(self):
        startup_service.user_service = user_service

    def test_should_get_true_when_superuser_exists(self):
        # given
        superuser_data = {
            "id": 0,
            "user_name": "superuser"
        }
        self.user_service_mock.get_user_by_user_name.return_value = superuser_data

        # when
        response = startup_service.superuser_exists()

        # then
        self.assertTrue(response)

    def test_should_get_false_when_superuser_does_not_exist(self):
        # given
        self.user_service_mock.get_user_by_user_name.return_value = None

        # when
        response = startup_service.superuser_exists()

        # then
        self.assertFalse(response)
