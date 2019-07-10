"""
The test module for the startup_service module.
"""

from unittest import mock

from tests import abstracts

from artushima import constants
from artushima.commons.exceptions import PersistenceError
from artushima.internal_services import user_internal_service
from artushima.services import startup_service


class CheckIfSuperuserExistsTest(abstracts.AbstractServiceTestClass):
    """
    Tests for the method startup_service.check_if_superuser_exists.
    """

    def setUp(self):
        super().setUp()

        self.user_internal_service_mock = mock.create_autospec(user_internal_service)
        startup_service.user_internal_service = self.user_internal_service_mock

    def tearDown(self):
        super().tearDown()

        startup_service.user_internal_service = user_internal_service

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
