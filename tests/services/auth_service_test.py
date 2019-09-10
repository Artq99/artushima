"""
The test module for the auth_service module.
"""

from unittest import mock

import flask
import werkzeug

from tests import abstracts

from artushima import constants
from artushima.internal_services import user_internal_service
from artushima.internal_services import auth_internal_service
from artushima.services import auth_service


class LogInTest(abstracts.AbstractServiceTestClass):
    """
    Tests for the method auth_service.log_in.
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

    def test_log_in_successful(self):
        """
        The test checks if the method can authenticate the user and generate an authentication token.
        """

        # given
        self.user_internal_service_mock.read_user_by_user_name.return_value = {
            "user_name": "test_user",
            "password_hash": "test_hash"
        }
        self.werkzeug_mock.check_password_hash.return_value = True
        self.auth_internal_service_mock.generate_token.return_value = b'test_token'

        # when
        response = auth_service.log_in("test_user", "password")

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
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
        self.auth_internal_service_mock.assert_not_called()
