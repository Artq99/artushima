"""
The test module for the auth_internal_service module.
"""

from unittest import mock
import datetime

import jwt

from tests import abstracts

from artushima.commons.exceptions import BusinessError
from artushima.commons import properties
from artushima.internal_services import auth_internal_service


class GenerateTokenTest(abstracts.AbstractServiceTestClass):
    """
    Tests for the method auth_internal_service.generate_token.

    The user data used in the tests contains only the user name, while the method does not need anything else in fact.
    """

    def setUp(self):
        super().setUp()

        self.properties_mock = mock.create_autospec(properties)
        self.jwt_mock = mock.create_autospec(jwt)
        self.datetime_mock = mock.create_autospec(datetime)
        self.datetime_mock.timedelta = datetime.timedelta
        auth_internal_service.properties = self.properties_mock
        auth_internal_service.jwt = self.jwt_mock
        auth_internal_service.datetime = self.datetime_mock

    def tearDown(self):
        super().tearDown()

        auth_internal_service.properties = properties
        auth_internal_service.jwt = jwt
        auth_internal_service.datetime = datetime

    def test_token_generated_correctly(self):
        """
        The test checks if the method generates a correct authentication token for the given user.
        """

        # given
        user_data = {
            "user_name": "test_user"
        }

        payload = {
            "sub": "test_user",
            "iat": datetime.datetime(2019, 1, 1),
            "exp": datetime.datetime(2019, 1, 1) + datetime.timedelta(minutes=60)
        }

        self.properties_mock.get_token_expiration_time.return_value = 60
        self.jwt_mock.encode.return_value = "test token"
        self.datetime_mock.datetime.utcnow.return_value = datetime.datetime(2019, 1, 1)

        # when
        token = auth_internal_service.generate_token(user_data)

        # then
        self.assertEqual("test token", token)
        self.properties_mock.get_token_expiration_time.assert_called_once()
        self.jwt_mock.encode.assert_called_once()
        args = self.jwt_mock.encode.call_args[0]
        self.assertEqual((payload), args[0])

    def test_user_data_is_none(self):
        """
        The test checks if the method raises an instance of BusinessError, when the given user_data is none.
        """

        # when then
        with self.assertRaises(BusinessError) as ctx:
            auth_internal_service.generate_token(None)

        self.assertEqual(
            "The argument 'user_data' cannot be None. "
            + "(artushima.internal_services.auth_internal_service.generate_token)",
            ctx.exception.message
        )
        self.properties_mock.get_token_expiration_time.assert_not_called()
        self.jwt_mock.encode.assert_not_called()

    def test_property_token_expiration_time_is_absent(self):
        """
        The test checks if the method raises an instance of BusinessError, when the property token_expiration_time
        is absent in the .env file.
        """

        # given
        user_data = {
            "user_name": "test_user"
        }
        self.properties_mock.get_token_expiration_time.return_value = None

        # when then
        with self.assertRaises(BusinessError) as ctx:
            auth_internal_service.generate_token(user_data)

        self.assertEqual(
            "The property 'token_expiration_time' is not present. "
            + "(artushima.internal_services.auth_internal_service.generate_token)",
            ctx.exception.message
        )
        self.properties_mock.get_token_expiration_time.assert_called_once()
        self.jwt_mock.encode.assert_not_called()
