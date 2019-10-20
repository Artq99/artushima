"""
The test module for the auth_service module.
"""

from unittest import mock

import flask

from tests import abstracts
from tests import test_utils
from tests import test_data_creator

from artushima import constants
from artushima import messages
from artushima.commons import properties
from artushima.internal_services import user_internal_service
from artushima.internal_services import auth_internal_service
from artushima.services import auth_service


class _TestCaseWithMocks(abstracts.AbstractServiceTestClass):
    """
    The base test case class with mocks prepared for tests of the auth_service module.
    """

    def setUp(self):
        super().setUp()

        self.flask_mock = mock.create_autospec(flask)
        self.properties_mock = mock.create_autospec(properties)
        self.user_internal_service_mock = mock.create_autospec(user_internal_service)
        self.auth_internal_service_mock = mock.create_autospec(auth_internal_service)
        auth_service.flask = self.flask_mock
        auth_service.properties = self.properties_mock
        auth_service.user_internal_service = self.user_internal_service_mock
        auth_service.auth_internal_service = self.auth_internal_service_mock

    def tearDown(self):
        super().tearDown()

        auth_service.flask = flask
        auth_service.properties = properties
        auth_service.user_internal_service = user_internal_service
        auth_service.auth_internal_service = auth_internal_service


class LogInTest(_TestCaseWithMocks):
    """
    Tests for the method auth_service.log_in.
    """

    def test_log_in_successful(self):
        """
        The test checks if the method can authenticate the user and generate an authentication token.
        """

        # given
        user = test_data_creator.create_test_user(1)
        password = "test_password_1"
        token = b"test_token_1"

        self.user_internal_service_mock.read_user_by_user_name.return_value = user.map_to_dict()
        self.auth_internal_service_mock.check_password.return_value = True
        self.auth_internal_service_mock.generate_token.return_value = token

        # when
        response = auth_service.log_in(user.user_name, password)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])

        expected_data = {
            "userName": user.user_name,
            "role": user.role,
            "token": token.decode()
        }
        self.assertEqual(expected_data, response["currentUser"])

    def test_user_name_is_missing(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the given user_name parameter is an empty string.
        """

        # given
        self.user_internal_service_mock.read_user_by_user_name.side_effect = \
            test_utils.create_missing_input_data_error("user_name")

        # when
        response = auth_service.log_in("", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.INPUT_DATA_MISSING.format(messages.ARG_NAMES["user_name"]), response["message"])

    def test_persistence_error_on_getting_user(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        a PersistenceError occurs on getting the user.
        """

        # given
        self.user_internal_service_mock.read_user_by_user_name.side_effect = test_utils.create_persistence_error()

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])

    def test_user_does_not_exist(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        a user for the given user name could not be found.
        """

        # given
        self.user_internal_service_mock.read_user_by_user_name.return_value = None

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.LOGIN_ERROR, response["message"])

    def test_incorrect_password(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the given password is incorrect.
        """

        # given
        user = test_data_creator.create_test_user(1)

        self.user_internal_service_mock.read_user_by_user_name.return_value = user.map_to_dict()
        self.auth_internal_service_mock.check_password.return_value = False

        # when
        response = auth_service.log_in(user.user_name, "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.LOGIN_ERROR, response["message"])

    def test_password_is_missing(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the give password is an empty string.
        """

        # given
        self.auth_internal_service_mock.check_password.side_effect = \
            test_utils.create_missing_input_data_error("password")

        # when
        response = auth_service.log_in("test_user", "")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.INPUT_DATA_MISSING.format(messages.ARG_NAMES["password"]), response["message"])


class LogOutTest(_TestCaseWithMocks):
    """
    Tests for the method auth_service.log_out.
    """

    def test_positive_output(self):
        """
        The test checks if the method gives a correct response after blacklisting a token.
        """

        # given
        blacklisted_token = test_data_creator.create_test_blacklisted_token(1)
        self.auth_internal_service_mock.blacklist_token.return_value = blacklisted_token.map_to_dict()

        # when
        response = auth_service.log_out(blacklisted_token.token)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertEqual(blacklisted_token.map_to_dict(), response["token"])

    def test_persistence_error(self):
        """
        The test checks if the method gives a correct response when a PersistenceError occurs.
        """

        # given
        self.auth_internal_service_mock.blacklist_token.side_effect = test_utils.create_persistence_error()

        # when
        response = auth_service.log_out("token")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])


class AuthenticateTest(_TestCaseWithMocks):
    """
    Tests for the method auth_service.authenticate.
    """

    def test_successful_authentication(self):
        """
        The test checks if the method correctly authenticates the given token.
        """

        # given
        token = "test_token"

        decoded_token = {
            "sub": "test_user"
        }

        user = {
            "id": 1,
            "user_name": "test_user"
        }

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = False
        self.auth_internal_service_mock.decode_token.return_value = decoded_token
        self.user_internal_service_mock.read_user_by_user_name.return_value = user

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])

    def test_token_is_blacklisted(self):
        """
        The test checks if the method returns a correct status and message when the given token has been blacklisted.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = True

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.AUTHENTICATION_FAILED, response["message"])

    def test_persistence_error_on_checking_if_token_is_blacklisted(self):
        """
        The test checks if the method returns a correct status and message when a PersistenceError occurs on checking
        if the given token has been blacklisted.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.check_if_token_is_blacklisted.side_effect = \
            test_utils.create_persistence_error()

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])

    def test_business_error_on_checking_if_token_is_blacklisted(self):
        """
        The test checks if the method returns a correct status and message when a BusinessError occurs on checking
        if the given token has been blacklisted.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.check_if_token_is_blacklisted.side_effect = \
            test_utils.create_business_error()

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.APPLICATION_ERROR, response["message"])

    def test_token_expired(self):
        """
        The test checks if the method returns a correct status and message when the given token has expired.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = False
        self.auth_internal_service_mock.decode_token.side_effect = test_utils.create_token_expiration_error()

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.TOKEN_EXPIRED, response["message"])

    def test_token_invalid(self):
        """
        The test checks if the method returns a correct status and message when the given token is invalid.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.decode_token.side_effect = test_utils.create_token_invalid_error()

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.AUTHENTICATION_FAILED, response["message"])

    def test_invalid_subject(self):
        """
        The test checks if the method returns a correct status and message when the given token contains an invalid
        subject.
        """

        # given
        token = "test_token"
        decoded_token = {
            "sub": "invalid_user"
        }

        self.auth_internal_service_mock.decode_token.return_value = decoded_token
        self.user_internal_service_mock.read_user_by_user_name.return_value = None

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.AUTHENTICATION_FAILED, response["message"])

    def test_persistence_error_on_getting_user(self):
        """
        The test checks if the method returns a correct status and message when a PersistencePerror occurs on getting
        the user from the repository.
        """

        # given
        token = "test_token"
        decoded_token = {
            "sub": "test_user"
        }

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = False
        self.auth_internal_service_mock.decode_token.return_value = decoded_token
        self.user_internal_service_mock.read_user_by_user_name.side_effect = test_utils.create_persistence_error()

        # when
        response = auth_service.authenticate(token, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])

    def test_successful_authentication_with_role(self):
        """
        The test checks if the method authenticates the given token and confirms, that the token bearer has the required
        role.
        """

        # given
        token = "test_token"

        decoded_token = {
            "sub": "test_user"
        }

        user = {
            "id": 1,
            "user_name": "test_user",
            "role": constants.ROLE_PLAYER
        }

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = False
        self.auth_internal_service_mock.decode_token.return_value = decoded_token
        self.user_internal_service_mock.read_user_by_user_name.return_value = user

        # when
        response = auth_service.authenticate(token, [constants.ROLE_PLAYER])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])

    def test_insufficient_role(self):
        """
        The test checks if the method returns a correct status and message when the user has an insufficient role.
        """

        # given
        token = "test_token"

        decoded_token = {
            "sub": "test_user"
        }

        user = {
            "id": 1,
            "user_name": "test_user",
            "role": constants.ROLE_PLAYER
        }

        self.auth_internal_service_mock.check_if_token_is_blacklisted.return_value = False
        self.auth_internal_service_mock.decode_token.return_value = decoded_token
        self.user_internal_service_mock.read_user_by_user_name.return_value = user

        # when
        response = auth_service.authenticate(token, [constants.ROLE_GAME_MASTER])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.ACCESS_DENIED, response["message"])

    def test_authenticate_test_bearer(self):
        """
        The test checks if the method authenticates the test bearer when it is enabled.
        """

        # given
        self.properties_mock.get_test_bearer_enabled.return_value = True

        # when
        response = auth_service.authenticate(constants.TEST_BEARER_TOKEN, [constants.ROLE_ADMIN])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])

    def test_test_bearer_not_enabled(self):
        """
        The test checks if the method returns a correct status and message on an attempt of authenticating with
        the test bearer token, when it is not enabled.
        """

        # given
        self.properties_mock.get_test_bearer_enabled.return_value = False

        # when
        response = auth_service.authenticate(constants.TEST_BEARER_TOKEN, [])

        # then
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.AUTHENTICATION_FAILED, response["message"])
