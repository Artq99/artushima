"""
The test module for the auth_internal_service module.
"""

from unittest import mock
import datetime

import jwt
import werkzeug

from tests import abstracts
from tests import test_data_creator

from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import MissingInputDataError
from artushima.commons.exceptions import MissingApplicationPropertyError
from artushima.commons.exceptions import InvalidApplicationPropertyValueError
from artushima.commons import properties
from artushima.persistence.dao import blacklisted_token_dao
from artushima.internal_services import auth_internal_service


class _TestCaseWithMocks(abstracts.AbstractServiceTestClass):
    """
    The base test case class with mocks prepared for tests of the auth_internal_service module.
    """

    def setUp(self):
        super().setUp()

        self.properties_mock = mock.create_autospec(properties)
        self.jwt_mock = mock.create_autospec(jwt)
        self.werkzeug_mock = mock.create_autospec(werkzeug)
        self.datetime_mock = mock.create_autospec(datetime)
        self.datetime_mock.timedelta = datetime.timedelta
        self.blacklisted_token_dao_mock = mock.create_autospec(blacklisted_token_dao)
        auth_internal_service.properties = self.properties_mock
        auth_internal_service.jwt = self.jwt_mock
        auth_internal_service.werkzeug = self.werkzeug_mock
        auth_internal_service.datetime = self.datetime_mock
        auth_internal_service.blacklisted_token_dao = self.blacklisted_token_dao_mock

    def tearDown(self):
        super().tearDown()

        auth_internal_service.properties = properties
        auth_internal_service.jwt = jwt
        auth_internal_service.werkzeug = werkzeug
        auth_internal_service.datetime = datetime
        auth_internal_service.blacklisted_token_dao = blacklisted_token_dao


class GenerateTokenTest(_TestCaseWithMocks):
    """
    Tests for the method auth_internal_service.generate_token.
    """

    def test_token_generated_correctly(self):
        """
        The test checks if the method generates a correct authentication token for the given user.
        """

        # given
        user_name = "test_user"

        payload = {
            "sub": "test_user",
            "iat": datetime.datetime(2019, 1, 1),
            "exp": datetime.datetime(2019, 1, 1) + datetime.timedelta(minutes=60)
        }

        self.properties_mock.get_token_expiration_time.return_value = 60
        self.jwt_mock.encode.return_value = "test token"
        self.datetime_mock.datetime.utcnow.return_value = datetime.datetime(2019, 1, 1)

        # when
        token = auth_internal_service.generate_token(user_name)

        # then
        self.assertEqual("test token", token)
        self.properties_mock.get_token_expiration_time.assert_called_once()
        self.jwt_mock.encode.assert_called_once()
        args = self.jwt_mock.encode.call_args[0]
        self.assertEqual((payload), args[0])

    def test_user_name_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given user name is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.generate_token(None)

    def test_user_name_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given user name is an empty
        string.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.generate_token("")

    def test_property_token_expiration_time_is_absent(self):
        """
        The test checks if the method raises an instance of MissingApplicationPropertyError when the property
        token_expiration_time is absent in the .env file.
        """

        # given
        user_name = "test_user"
        self.properties_mock.get_token_expiration_time.return_value = None

        # when then
        with self.assertRaises(MissingApplicationPropertyError):
            auth_internal_service.generate_token(user_name)

    def test_property_token_expiration_time_has_invalid_value(self):
        """
        The test checks if the method raises an instance of InvalidApplicationPropertyValueError when the property
        token_expiration_time has an invalid value assigned.
        """

        # given
        user_name: str = "test_user"
        self.properties_mock.get_token_expiration_time.return_value = "invalid"

        # when then
        with self.assertRaises(InvalidApplicationPropertyValueError):
            auth_internal_service.generate_token(user_name)


class BlacklistTokenTest(_TestCaseWithMocks):
    """
    Tests for the method auth_internal_service.blacklist_token.
    """

    def test_blacklist(self):
        """
        The test checks if the method correctly calls the DAO to persist the given token as blacklisted.
        """

        # given
        token = "test_token"
        persisted_token = {
            "id": 1,
            "token": token
        }
        self.blacklisted_token_dao_mock.create.return_value = persisted_token

        # when
        response = auth_internal_service.blacklist_token(token)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(persisted_token, response)
        self.blacklisted_token_dao_mock.create.assert_called_once_with(token)

    def test_token_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given token is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.blacklist_token(None)

    def test_token_is_empty(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given token is an empty
        string.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.blacklist_token("")


class CheckIfTokenIsBlacklistedTest(_TestCaseWithMocks):
    """
    Tests for the method auth_internal_service.check_if_token_is_blacklisted.
    """

    def test_token_is_blacklisted(self):
        """
        The test checks if the method returns True if the token has been blacklisted.
        """

        # given
        self.blacklisted_token_dao_mock.read_by_token.return_value = test_data_creator.create_test_blacklisted_token(1)

        # when
        response = auth_internal_service.check_if_token_is_blacklisted("token_1")

        # then
        self.assertTrue(response)

    def test_token_is_not_blacklisted(self):
        """
        The test checks if the method returns False if the token has not been blacklisted.
        """

        # given
        self.blacklisted_token_dao_mock.read_by_token.return_value = None

        # when
        response = auth_internal_service.check_if_token_is_blacklisted("token_1")

        # then
        self.assertFalse(response)

    def test_token_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given token is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_if_token_is_blacklisted(None)

    def test_token_is_empty(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given token is an empty
        string.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_if_token_is_blacklisted("")


class DecodeTokenTest(_TestCaseWithMocks):
    """
    Test for the method auth_internal_service.decode_token.
    """

    def test_correctly_decoded_token(self):
        """
        The test checks if the method can decode a token correctly.
        """

        # given
        token = "test_token"
        self.properties_mock.get_app_secret_key.return_value = "secret"
        self.jwt_mock.decode.return_value = "decoded_token"

        # when
        decoded_token = auth_internal_service.decode_token(token)

        # then
        self.assertEqual("decoded_token", decoded_token)
        self.properties_mock.get_app_secret_key.assert_called_once()
        self.jwt_mock.decode.assert_called_once_with(token, "secret", algorithm="HS256")

    def test_expired_signature(self):
        """
        The test checks if the method raises a BusinessError, when the token signature has expired.
        """

        # given
        token = "test_token"
        self.properties_mock.get_app_secret_key.return_value = "secret"
        self.jwt_mock.decode.side_effect = jwt.ExpiredSignatureError()

        # when then
        with self.assertRaises(BusinessError) as ctx:
            auth_internal_service.decode_token(token)

        self.assertEqual(
            "Authentication token signature has expired. " +
            "(artushima.internal_services.auth_internal_service.decode_token)",
            ctx.exception.message
        )

    def test_invalid_token(self):
        """
        The test checks if the method raises a BusinessError, when the token is invalid.
        """

        # given
        token = "test_token"
        self.properties_mock.get_app_secret_key.return_value = "secret"
        self.jwt_mock.decode.side_effect = jwt.InvalidTokenError()

        # when then
        with self.assertRaises(BusinessError) as ctx:
            auth_internal_service.decode_token(token)

        self.assertEqual(
            "The token is invalid. (artushima.internal_services.auth_internal_service.decode_token)",
            ctx.exception.message
        )


class CheckPasswordTest(_TestCaseWithMocks):
    """
    Tests for the method auth_internal_service.check_password.
    """

    def test_check_password_successful(self):
        """
        The test checks if the werkzeug has been called correctly.
        """

        # given
        self.werkzeug_mock.check_password_hash.return_value = True

        # when
        response = auth_internal_service.check_password("password", "hash")

        # then
        self.assertIsNotNone(response)
        self.assertTrue(response)
        self.werkzeug_mock.check_password_hash.assert_called_once_with("hash", "password")

    def test_password_is_none(self):
        """
        The test checks if the method raises a MissingInputDataError when the given password is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_password(None, "hash")

    def test_password_is_empty(self):
        """
        The test checks if the method raises a MissingInputDataError when the given password is an empty string.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_password("", "hash")

    def test_hash_is_none(self):
        """
        The test checks if the method raises a MissingInputDataError when the given hash is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_password("password", None)

    def test_hash_is_empty(self):
        """
        The test checks if the method raises a MissingInputDataError when the given hash is an empty string.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            auth_internal_service.check_password("password", "")
