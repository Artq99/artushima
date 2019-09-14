"""
The test module for the auth_service module.
"""

from unittest import mock

import flask
import werkzeug

from tests import abstracts
from tests import test_utils

from artushima import constants
from artushima import messages
from artushima.commons.exceptions import PersistenceError
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
        self.werkzeug_mock = mock.create_autospec(werkzeug)
        self.user_internal_service_mock = mock.create_autospec(user_internal_service)
        self.auth_internal_service_mock = mock.create_autospec(auth_internal_service)
        auth_service.flask = self.flask_mock
        auth_service.werkzeug = self.werkzeug_mock
        auth_service.user_internal_service = self.user_internal_service_mock
        auth_service.auth_internal_service = self.auth_internal_service_mock

    def tearDown(self):
        super().tearDown()

        auth_service.flask = flask
        auth_service.werkzeug = werkzeug
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
        self.user_internal_service_mock.read_user_by_user_name.return_value = {
            "user_name": "test_user",
            "role": constants.ROLE_PLAYER,
            "password_hash": "test_hash"
        }
        self.werkzeug_mock.check_password_hash.return_value = True
        self.auth_internal_service_mock.generate_token.return_value = b'test_token'

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertEqual({
            "userName": "test_user",
            "role": "role_player",
            "token": 'test_token'
        }, response["currentUser"])
        self.user_internal_service_mock.read_user_by_user_name.assert_called_once_with("test_user")
        self.werkzeug_mock.check_password_hash.assert_called_once_with("test_hash", "password")

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
        self.assertEqual("Niepoprawny login lub hasło.", response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_called_once_with("test_user")
        self.werkzeug_mock.check_password_hash.assert_not_called()
        self.auth_internal_service_mock.assert_not_called()

    def test_incorrect_password(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the given password is incorrect.
        """

        # given
        self.user_internal_service_mock.read_user_by_user_name.return_value = {
            "user_name": "test_user",
            "password_hash": "test_hash"
        }
        self.werkzeug_mock.check_password_hash.return_value = False

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Niepoprawny login lub hasło.", response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_called_once_with("test_user")
        self.werkzeug_mock.check_password_hash.assert_called_once_with("test_hash", "password")
        self.auth_internal_service_mock.assert_not_called()

    def test_user_name_is_none(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the given user_name parameter is None.
        """

        # when
        response = auth_service.log_in(None, "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Brakująca nazwa użytkownika.", response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_not_called()
        self.werkzeug_mock.check_password_hash.assert_not_called()
        self.auth_internal_service_mock.assert_not_called()

    def test_password_is_none(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        the given password is None.
        """

        # when
        response = auth_service.log_in("test_user", None)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Brakujące hasło.", response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_not_called()
        self.werkzeug_mock.check_password_hash.assert_not_called()
        self.auth_internal_service_mock.generate_token.assert_not_called()

    def test_persistence_error_on_getting_user(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        a PersistenceError occurs.
        """

        # given
        user_name = "test_user"
        password = "test_password"

        self.user_internal_service_mock.read_user_by_user_name.side_effect = test_utils.create_persistence_error()

        # when
        response = auth_service.log_in(user_name, password)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_called_once_with(user_name)
        self.werkzeug_mock.check_password_hash.assert_not_called()
        self.auth_internal_service_mock.generate_token.assert_not_called()

    def test_business_error_on_getting_user(self):
        """
        The test checks if the method returns a response with the status failure and a correct error message, when
        a BusinessError occurs.
        """

        # given
        user_name = "test_user"
        password = "test_password"

        self.user_internal_service_mock.read_user_by_user_name.side_effect = test_utils.create_business_error()

        # when
        response = auth_service.log_in(user_name, password)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.APPLICATION_ERROR, response["message"])
        self.user_internal_service_mock.read_user_by_user_name.assert_called_once_with(user_name)
        self.werkzeug_mock.check_password_hash.assert_not_called()
        self.auth_internal_service_mock.generate_token.assert_not_called()


class LogOutTest(_TestCaseWithMocks):
    """
    Tests for the method auth_service.log_out.
    """

    def test_positive_output(self):
        """
        The test checks if the method gives a correct response after blacklisting a token.
        """

        # given
        token = "test_token"
        peristed_token = {
            "id": 1,
            "token": token
        }

        self.auth_internal_service_mock.blacklist_token.return_value = peristed_token

        # when
        response = auth_service.log_out(token)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertEqual(peristed_token, response["token"])
        self.auth_internal_service_mock.blacklist_token.assert_called_once_with(token)

    def test_persistence_error(self):
        """
        The test checks if the method gives a correct response when a PersistenceError occurs.
        """

        # given
        token = "test_token"

        self.auth_internal_service_mock.blacklist_token.side_effect = PersistenceError("Test.", "TestClass", "test")

        # when
        response = auth_service.log_out(token)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual(messages.PERSISTENCE_ERROR, response["message"])
        self.auth_internal_service_mock.blacklist_token.assert_called_once_with(token)
