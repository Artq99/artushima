"""
The testing module for the startup service.
"""

from unittest import TestCase
from unittest.mock import create_autospec

from artushima.core import properties
from artushima.startup import startup_service
from artushima.user import user_service
from artushima.user.roles import ALL_ROLES


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


class CreateSuperuserTest(TestCase):

    def setUp(self):
        self.user_service_mock = create_autospec(user_service)
        self.properties_mock = create_autospec(properties)
        startup_service.user_service = self.user_service_mock
        startup_service.properties = self.properties_mock

    def tearDown(self):
        startup_service.user_service = user_service
        startup_service.properties = properties

    def test_should_create_superuser(self):
        # given
        self.properties_mock.get_superuser_password.return_value = "superuser_password"

        # when
        startup_service.create_superuser()

        # then
        self.user_service_mock.create_user.assert_called_once()
        args = self.user_service_mock.create_user.call_args
        editor_name = args[0][0]
        user_name = args[0][1]
        password = args[0][2]
        roles = args[1]["roles"]

        self.assertEqual("SYSTEM", editor_name)
        self.assertEqual("superuser", user_name)
        self.assertEqual("superuser_password", password)
        self.assertEqual(ALL_ROLES, roles)

    def test_should_raise_error_when_superuser_password_is_missing(self):
        # given
        self.properties_mock.get_superuser_password.return_value = None

        # when then
        with self.assertRaises(RuntimeError):
            startup_service.create_superuser()
