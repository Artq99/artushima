"""
The test module for the user_internal_service module.
"""

from unittest import mock

from tests import abstracts

from artushima import constants
from artushima.commons.exceptions import BusinessError
from artushima.persistence.dao import user_dao
from artushima.internal_services import user_internal_service


class _TestCaseWithMocks(abstracts.AbstractServiceTestClass):
    """
    The base test case class with mocks prepared for tests of the user_internal_service module.
    """

    def setUp(self):
        super().setUp()

        self.user_dao_mock = mock.create_autospec(user_dao)
        user_internal_service.user_dao = self.user_dao_mock

    def tearDown(self):
        super().tearDown()

        user_internal_service.user_dao = user_dao


class CheckIfUserExistsTest(_TestCaseWithMocks):
    """
    Tests for the method user_internal_service.check_if_user_exists.
    """

    def test_response_true(self):
        """
        The test checks if the method returns True, when the user of the given user name exists in the database.
        """

        # given
        user_name = "test_user"

        self.user_dao_mock.read_by_user_name.return_value = {
            "id": 1,
            "user_name": user_name
        }

        # when
        user_exists = user_internal_service.check_if_user_exists(user_name)

        # then
        self.assertTrue(user_exists)
        self.user_dao_mock.read_by_user_name.assert_called_once_with(user_name)

    def test_response_false(self):
        """
        The test checks if the method returns False, when the user of the given user name does not exist in the
        database.
        """

        # given
        user_name = "test_user"

        self.user_dao_mock.read_by_user_name.return_value = None

        # when
        user_exists = user_internal_service.check_if_user_exists(user_name)

        # then
        self.assertFalse(user_exists)
        self.user_dao_mock.read_by_user_name.assert_called_once_with(user_name)

    def test_user_name_is_none(self):
        """
        The test checks if the method raises a BusinessError, when the given user name is None.
        """

        # given
        username = None

        # when then
        with self.assertRaises(BusinessError) as ctx:
            user_internal_service.check_if_user_exists(username)

        self.assertEqual(
            "The argument 'user_name' cannot be None. "
            + "(artushima.internal_services.user_internal_service.check_if_user_exists)",
            ctx.exception.message
        )
        self.user_dao_mock.read_by_user_name.assert_not_called()


class CreateUserTest(_TestCaseWithMocks):
    """
    Tests for the method user_internal_service_test.create_user.
    """

    def test_positive_output(self):
        """
        The test checks if the method correctly calls the corresponding repository.
        """

        # given
        data = {
            "user_name": "test_user",
            "password_hash": "test_hash",
            "role": constants.ROLE_PLAYER
        }

        self.user_dao_mock.create.return_value = {
            "id": 1,
            "user_name": "test_user",
            "password_hash": "test_hash",
            "role": constants.ROLE_PLAYER
        }

        # when
        user_internal_service.create_user(data)

        # then
        self.user_dao_mock.create.assert_called_once_with(data)


class ReadUserByUserNameTest(_TestCaseWithMocks):
    """
    Tests for the method user_internal_service_test.read_user_by_user_name.
    """

    def test_positive_output(self):
        """
        The test checks if the method correctly calls the corresponding repository.
        """

        # given
        self.user_dao_mock.read_by_user_name.return_value = {
            "id": 1,
            "user_name": "test_user",
            "password_hash": "test_hash",
            "role": constants.ROLE_PLAYER
        }

        # when
        user = user_internal_service.read_user_by_user_name("test_user")

        # then
        self.assertIsNotNone(user)
        self.user_dao_mock.read_by_user_name.assert_called_once_with("test_user")
