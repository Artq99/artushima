"""
The test module for the startup_service module.
"""

from unittest import mock

from werkzeug import security

from tests import abstracts

from artushima import constants
from artushima.commons import properties
from artushima.commons.exceptions import PersistenceError
from artushima.internal_services import user_internal_service
from artushima.internal_services import user_history_internal_service
from artushima.services import startup_service


class _TestCaseWithMocks(abstracts.AbstractServiceTestClass):
    """
    The base test case class with mocks prepared for tests of the startup_service module.
    """

    def setUp(self):
        super().setUp()

        self.security_mock = mock.create_autospec(security)
        self.properties_mock = mock.create_autospec(properties)
        self.user_internal_service_mock = mock.create_autospec(user_internal_service)
        self.user_history_internal_service_mock = mock.create_autospec(user_history_internal_service)

        startup_service.security = self.security_mock
        startup_service.properties = self.properties_mock
        startup_service.user_internal_service = self.user_internal_service_mock
        startup_service.user_history_internal_service = self.user_history_internal_service_mock

    def tearDown(self):
        super().tearDown()

        startup_service.user_internal_service = user_internal_service


class CheckIfSuperuserExistsTest(_TestCaseWithMocks):
    """
    Tests for the method startup_service.check_if_superuser_exists.
    """

    def test_response_true(self):
        """
        The test checks if the method returns a correct response, when the superuser exists.
        """

        # given
        self.user_internal_service_mock.check_if_user_exists.return_value = True

        # when
        response = startup_service.check_if_superuser_exists()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertTrue(response["superuser_exists"])
        self.user_internal_service_mock.check_if_user_exists.assert_called_once_with("superuser")

    def test_response_false(self):
        """
        The test checks if the method returns a correct response, when the superuser does not exist.
        """

        # given
        self.user_internal_service_mock.check_if_user_exists.return_value = False

        # when
        response = startup_service.check_if_superuser_exists()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertFalse(response["superuser_exists"])
        self.user_internal_service_mock.check_if_user_exists.assert_called_once_with("superuser")

    def test_persistence_error(self):
        """
        The test checks if the method returns a correct response, when a PersistenceError occures.
        """

        # given
        self.user_internal_service_mock.check_if_user_exists.side_effect = PersistenceError(
            "test", "TestClass", "test_method"
        )

        # when
        response = startup_service.check_if_superuser_exists()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Błąd odczytu danych.", response["message"])
        self.user_internal_service_mock.check_if_user_exists.assert_called_once_with("superuser")


class CreateSuperuserTest(_TestCaseWithMocks):
    """
    Tests for the method startup_service.create_superuser.
    """

    def test_positive_output(self):
        """
        The test checks if the method creates superuser and returns successful response.
        """

        # given
        self.properties_mock.get_superuser_password.return_value = "password"
        self.security_mock.generate_password_hash.return_value = "hash"
        self.user_internal_service_mock.create_user.return_value = {
            "id": 1,
            "user_name": "superuser",
            "password_hash": "hash"
        }
        self.user_history_internal_service_mock.create_user_history_entry.return_value = {
            "id": 1,
            "editor_name": "System",
            "message": "Superużytkownik został utworzony.",
            "user_id": 1
        }

        # when
        response = startup_service.create_superuser()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_SUCCESS, response["status"])
        self.assertIsNone(response["message"])
        self.properties_mock.get_superuser_password.assert_called_once()
        self.security_mock.generate_password_hash.assert_called_once_with("password")
        self.user_internal_service_mock.create_user.assert_called_once_with({
            "user_name": "superuser",
            "password_hash": "hash",
            "role": constants.ROLE_ADMIN
        })
        self.user_history_internal_service_mock.create_user_history_entry.assert_called_once_with({
            "editor_name": "System",
            "message": "Superużytkownik został utworzony.",
            "user_id": 1
        })

    def test_superuser_password_is_none(self):
        """
        The test checks if the method returns failure, when the superuser password has not been given in the properties.
        """

        # given
        self.properties_mock.get_superuser_password.return_value = None

        # when
        response = startup_service.create_superuser()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Brakujące dane: hasło dla superużytkownika.", response["message"])
        self.security_mock.generate_password_hash.assert_not_called()
        self.user_internal_service_mock.create_user.assert_not_called()
        self.user_history_internal_service_mock.create_user_history_entry.assert_not_called()

    def test_persistence_error_on_create_user(self):
        """
        The test checks if the method returns failure, when a persistence error occurs on creating user.
        """

        # given
        self.properties_mock.get_superuser_password.return_value = "password"
        self.security_mock.generate_password_hash.return_value = "hash"
        self.user_internal_service_mock.create_user.side_effect = PersistenceError(
            "test", "TestClass", "test_method"
        )

        # when
        response = startup_service.create_superuser()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Superużytkownik nie mógł zostać utworzony.", response["message"])
        self.security_mock.generate_password_hash.assert_called_once()
        self.user_internal_service_mock.create_user.assert_called_once()
        self.user_history_internal_service_mock.create_user_history_entry.assert_not_called()

    def test_persistence_error_on_create_user_history_entry(self):
        """
        The test checks if the method returns failure, when a persistence error occurs on creating user history entry.
        """

        # given
        self.properties_mock.get_superuser_password.return_value = "password"
        self.security_mock.generate_password_hash.return_value = "hash"
        self.user_internal_service_mock.create_user.return_value = {
            "id": 1,
            "user_name": "superuser",
            "password_hash": "hash"
        }
        self.user_history_internal_service_mock.create_user_history_entry.side_effect = PersistenceError(
            "test", "TestClass", "test_method"
        )

        # when
        response = startup_service.create_superuser()

        # then
        self.assertIsNotNone(response)
        self.assertEqual(constants.RESPONSE_STATUS_FAILURE, response["status"])
        self.assertEqual("Wpis do historii dla superużytkownika nie mógł zostać utworzony.", response["message"])
        self.security_mock.generate_password_hash.assert_called_once()
        self.user_internal_service_mock.create_user.assert_called_once()
        self.user_history_internal_service_mock.create_user_history_entry.assert_called_once()
