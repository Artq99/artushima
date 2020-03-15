"""
The testing module for the auth service.
"""

from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import create_autospec

import jwt
import werkzeug
from jwt import ExpiredSignatureError, InvalidTokenError

from artushima.auth import auth_service
from artushima.auth.persistence import blacklisted_token_repository
from artushima.auth.persistence.model import BlacklistedTokenEntity
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
        auth_service.jwt = jwt

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


class IsTokenOkTest(TestCase):

    def setUp(self):
        self.jwt_mock = create_autospec(jwt)
        self.properties_mock = create_autospec(properties)
        self.blacklisted_token_repository_mock = create_autospec(blacklisted_token_repository)
        self.user_service_mock = create_autospec(user_service)
        auth_service.jwt = self.jwt_mock
        auth_service.properties = self.properties_mock
        auth_service.blacklisted_token_repository = self.blacklisted_token_repository_mock
        auth_service.user_service = self.user_service_mock

    def tearDown(self):
        auth_service.jwt = jwt
        auth_service.properties = properties
        auth_service.blacklisted_token_repository = blacklisted_token_repository
        auth_service.user_service = user_service

    def test_should_not_authenticate_token_when_it_is_none(self):
        # given
        token = None

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_authenticate_test_bearer(self):
        # given
        token = "Bearer " + auth_service.TEST_BEARER_TOKEN
        self.properties_mock.get_test_bearer_enabled.return_value = True

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertTrue(response)

    def test_should_not_authenticate_test_bearer(self):
        # given
        token = "Bearer " + auth_service.TEST_BEARER_TOKEN
        self.properties_mock.get_test_bearer_enabled.return_value = False

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_blacklisted_token(self):
        # given
        token = "Bearer test"
        blacklisted_token = BlacklistedTokenEntity()
        blacklisted_token.token = token

        self.blacklisted_token_repository_mock.read_by_token.return_value = blacklisted_token

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_expired_token(self):
        # given
        token = "Bearer test"

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.side_effect = ExpiredSignatureError

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_invalid_token(self):
        # given
        token = "Bearer test"

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.side_effect = InvalidTokenError

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_invalid_sub(self):
        # given
        token = "Bearer test"

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.return_value = {
            "iat": datetime.utcnow() - timedelta(minutes=10),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "sub": "test_user"
        }

        self.user_service_mock.get_user_by_user_name.return_value = None

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertFalse(response)

    def test_should_authenticate_token(self):
        # given
        token = "Bearer test"

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.return_value = {
            "iat": datetime.utcnow() - timedelta(minutes=10),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "sub": "test_user"
        }
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 1,
            "user_name": "test_user"
        }

        # when
        response = auth_service.is_token_ok(token)

        # then
        self.assertTrue(response)


class GetUserNameTest(TestCase):

    def setUp(self):
        self.jwt_mock = create_autospec(jwt)
        auth_service.jwt = self.jwt_mock

    def tearDown(self):
        auth_service.jwt = jwt

    def test_should_return_none_when_token_is_none(self):
        # given
        token = None

        # when
        result = auth_service.get_user_name(token)

        # then
        self.assertIsNone(result)

    def test_should_return_test_when_token_is_test_bearer_token(self):
        # given
        token = f"Bearer {auth_service.TEST_BEARER_TOKEN}"

        # when
        result = auth_service.get_user_name(token)

        # then
        self.assertEqual("Test", result)

    def test_should_return_none_when_token_is_invalid(self):
        # given
        token = "Bearer test"
        self.jwt_mock.decode.side_effect = InvalidTokenError()

        # when
        result = auth_service.get_user_name(token)

        # then
        self.assertIsNone(result)

    def test_should_return_user_name(self):
        # given
        token = "Bearer test"
        self.jwt_mock.decode.return_value = {"sub": "test_user"}

        # when
        result = auth_service.get_user_name(token)

        # then
        self.assertEqual("test_user", result)


class GetUserIdTest(TestCase):

    def setUp(self):
        self.jwt_mock = create_autospec(jwt)
        self.user_service_mock = create_autospec(user_service)
        auth_service.jwt = self.jwt_mock
        auth_service.user_service = self.user_service_mock

    def tearDown(self):
        auth_service.jwt = jwt
        auth_service.user_service = user_service

    def test_should_get_user_id(self):
        # given
        token = "Bearer test"
        self.jwt_mock.decode.return_value = {"sub": "test_user"}
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 100,
            "user_name": "test_user"
        }

        # when
        result = auth_service.get_user_id(token)

        # then
        self.assertIsNotNone(result)
        self.assertEqual(100, result)
        self.user_service_mock.get_user_by_user_name.assert_called_once_with("test_user")

    def test_should_get_none_when_token_is_none(self):
        # given
        token = None

        # when
        result = auth_service.get_user_id(token)

        # then
        self.assertIsNone(result)

    def test_should_get_superuser_id_when_token_is_test_bearer_token(self):
        # given
        token = f"Bearer {auth_service.TEST_BEARER_TOKEN}"
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 1,
            "user_name": "superuser"
        }

        # when
        result = auth_service.get_user_id(token)

        # then
        self.assertIsNotNone(result)
        self.assertEqual(1, result)
        self.jwt_mock.decode.assert_not_called()
        self.user_service_mock.get_user_by_user_name.assert_called_once_with("superuser")

    def test_should_get_none_when_token_is_invalid(self):
        # given
        token = "Bearer test"
        self.jwt_mock.decode.side_effect = InvalidTokenError()

        # when
        result = auth_service.get_user_id(token)

        # then
        self.assertIsNone(result)

    def test_should_get_none_when_user_does_not_exist(self):
        # given
        token = "Bearer test"
        self.jwt_mock.decode.return_value = {
            "sub": "test_user"
        }
        self.user_service_mock.get_user_by_user_name.return_value = None

        # when
        result = auth_service.get_user_id(token)

        # then
        self.assertIsNone(result)


class AreRolesSufficientTest(TestCase):

    def setUp(self):
        self.jwt_mock = create_autospec(jwt)
        self.properties_mock = create_autospec(properties)
        self.blacklisted_token_repository_mock = create_autospec(blacklisted_token_repository)
        self.user_service_mock = create_autospec(user_service)
        self.user_roles_service_mock = create_autospec(user_roles_service)
        auth_service.jwt = self.jwt_mock
        auth_service.properties = self.properties_mock
        auth_service.blacklisted_token_repository = self.blacklisted_token_repository_mock
        auth_service.user_service = self.user_service_mock
        auth_service.user_roles_service = self.user_roles_service_mock

    def tearDown(self):
        auth_service.jwt = jwt
        auth_service.properties = properties
        auth_service.blacklisted_token_repository = blacklisted_token_repository
        auth_service.user_service = user_service
        auth_service.user_roles_service = user_roles_service

    def test_should_return_true_when_no_roles_are_required(self):
        # given
        token = "Bearer test"
        required_roles = []

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertTrue(response)

    def test_should_return_false_when_token_is_none(self):
        # given
        token = None
        required_roles = ["role_test"]

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_return_false_when_no_roles_are_required_and_token_is_none(self):
        # given
        token = None
        required_roles = []

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_authenticate_test_bearer(self):
        # given
        token = "Bearer " + auth_service.TEST_BEARER_TOKEN
        required_roles = ["role_test"]

        self.properties_mock.get_test_bearer_enabled.return_value = True

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertTrue(response)

    def test_should_not_authenticate_test_bearer(self):
        # given
        token = "Bearer " + auth_service.TEST_BEARER_TOKEN
        required_roles = ["role_test"]

        self.properties_mock.get_test_bearer_enabled.return_value = False

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_blacklisted_token(self):
        # given
        token = "Bearer test"
        required_roles = ["role_test"]

        blacklisted_token = BlacklistedTokenEntity()
        blacklisted_token.token = "test"

        self.blacklisted_token_repository_mock.read_by_token.return_value = blacklisted_token

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_expired_token(self):
        # given
        token = "Bearer test"
        required_roles = ["role_test"]

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.side_effect = ExpiredSignatureError

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_not_authenticate_invalid_sub(self):
        # given
        token = "Bearer test"
        required_roles = ["role_test"]

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.return_value = {
            "iat": datetime.utcnow() - timedelta(minutes=10),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "sub": "test_user"
        }

        self.user_service_mock.get_user_by_user_name.return_value = None

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_return_false_when_roles_are_not_sufficient(self):
        # given
        token = "Bearer test"
        required_roles = ["role_test"]

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.return_value = {
            "iat": datetime.utcnow() - timedelta(minutes=10),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "sub": "test_user"
        }
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 1,
            "user_name": "test_user"
        }
        self.user_roles_service_mock.get_user_roles.return_value = [
            "role_test_2",
            "tole_test_3"
        ]

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertFalse(response)

    def test_should_authenticate_user_with_sufficient_roles(self):
        # given
        token = "Bearer test"
        required_roles = ["role_test"]

        self.blacklisted_token_repository_mock.read_by_token.return_value = None
        self.jwt_mock.decode.return_value = {
            "iat": datetime.utcnow() - timedelta(minutes=10),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "sub": "test_user"
        }
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 1,
            "user_name": "test_user"
        }
        self.user_roles_service_mock.get_user_roles.return_value = [
            "role_test",
            "role_test_2",
            "tole_test_3"
        ]

        # when
        response = auth_service.are_roles_sufficient(token, required_roles)

        # then
        self.assertTrue(response)


class BlacklistTokenTest(TestCase):

    def setUp(self):
        self.blacklisted_token_repository_mock = create_autospec(blacklisted_token_repository)
        auth_service.blacklisted_token_repository = self.blacklisted_token_repository_mock

    def tearDown(self):
        auth_service.blacklisted_token_repository = blacklisted_token_repository

    def test_should_blacklist_token(self):
        # given
        token = "Bearer test-token"

        # when
        auth_service.blacklist_token(token)

        # then
        self.blacklisted_token_repository_mock.persist.assert_called_once()

        blacklisted_token = self.blacklisted_token_repository_mock.persist.call_args[0][0]
        self.assertIsInstance(blacklisted_token, BlacklistedTokenEntity)
        self.assertEqual("test-token", blacklisted_token.token)
