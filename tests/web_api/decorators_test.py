"""
The testing module for the decorators of the web_api package.
"""

from unittest import mock

import flask
import werkzeug

from tests import abstracts

from artushima.web_api import decorators
from artushima.services import auth_service
from artushima.services import service_utils

auth_required = decorators.auth_required


class AuthRequiredTest(abstracts.AbstractTestClass):
    """
    Tests for the decorator auth_required.
    """

    def setUp(self):
        super().setUp()

        self.flask_mock = mock.create_autospec(flask)
        self.auth_service_mock = mock.create_autospec(auth_service)
        decorators.flask = self.flask_mock
        decorators.auth_service = self.auth_service_mock

    def tearDown(self):
        super().tearDown()

        decorators.flask = flask
        decorators.auth_service = auth_service

    def test_header_missing(self):
        """
        The test checks if the decorator aborts the request if the authorization header is missing.
        """

        # given
        request = flask.Request(dict())
        request.headers = werkzeug.Headers()

        self.flask_mock.request = request
        self.flask_mock.abort.return_value = "failure"

        @auth_required()
        def web_method():
            return "success"

        # when
        response = web_method()

        # then
        self.assertEqual("failure", response)
        self.flask_mock.abort.assert_called_once_with(401)

    def test_success(self):
        """
        The test checks if the decorator allows the method to execute, when authentication was successful.
        """

        # given
        request = flask.Request(dict())
        headers = werkzeug.Headers()
        headers.add("Authorization", "Bearer token")
        request.headers = headers

        self.flask_mock.request = request
        self.auth_service_mock.authenticate.return_value = service_utils.create_response_success()

        @auth_required()
        def web_method():
            return "success"

        # when
        response = web_method()

        # then
        self.assertEqual("success", response)

    def test_failure(self):
        """
        The test checks if the decorator aborts the request, when authentication was unsuccessful.
        """

        # given
        request = flask.Request(dict())
        headers = werkzeug.Headers()
        headers.add("Authorization", "Bearer token")
        request.headers = headers

        self.flask_mock.request = request
        self.flask_mock.abort.return_value = "failure"
        self.auth_service_mock.authenticate.return_value = service_utils.create_response_failure()

        @auth_required()
        def web_method():
            return "success"

        # when
        response = web_method()

        # then
        self.assertEqual("failure", response)
        self.flask_mock.abort.assert_called_once_with(401)
