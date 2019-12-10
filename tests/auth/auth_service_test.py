"""
The testing module for the auth service.
"""

from unittest import TestCase
from unittest.mock import create_autospec

import jwt
import werkzeug

from artushima.auth import auth_service
from artushima.core import properties
from artushima.core.exceptions import BusinessError
from artushima.user import user_roles_service, user_service


class LogInTest(TestCase):

    def setUp(self):
        self.user_service_mock = create_autospec(user_service)
        self.user_roles_service_mock = create_autospec(user_roles_service)
        self.properties_mock = create_autospec(properties)
        self.werkzeug_mock = create_autospec(werkzeug)
        self.jwt_mock = create_autospec(jwt)
        auth_service.user_service = self.user_service_mock
        auth_service.user_roles_service = self.user_roles_service_mock
        auth_service.properties = self.properties_mock
        auth_service.werkzeug = self.werkzeug_mock
        auth_service.jwt = self.jwt_mock

    def tearDown(self):
        auth_service.user_service = user_service
        auth_service.user_roles_service = user_roles_service
        auth_service.werkzeug = werkzeug
        auth_service.properties = properties
        auth_service.jwt = self.jwt_mock

    def test_should_authenticate_user(self):
        # given
        self.properties_mock.get_token_expiration_time.return_value = "60"
        self.properties_mock.get_app_secret_key.return_value = "secret"

        self.jwt_mock.encode.return_value = b"test_token"

        self.user_roles_service_mock.get_user_roles.return_value = {
            "test_role_1",
            "test_role_2"
        }

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertEqual("test_user", response["user_name"])
        self.assertEqual("test_token", response["token"])
        self.assertEqual(2, len(response["roles"]))
        self.assertIn("test_role_1", response["roles"])
        self.assertIn("test_role_2", response["roles"])

    def test_should_raise_error_when_user_does_not_exist(self):
        # given
        self.user_service_mock.get_user_by_user_name.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            auth_service.log_in("test_user", "password")

    def test_should_raise_error_when_password_is_incorrect(self):
        # given
        self.werkzeug_mock.check_password_hash.return_value = False

        # when then
        with self.assertRaises(BusinessError):
            auth_service.log_in("test_user", "password")
