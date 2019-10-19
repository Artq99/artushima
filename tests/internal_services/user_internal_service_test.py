"""
The test module for the user_internal_service module.
"""

from unittest import mock

from tests import abstracts
from tests import test_data_creator

from artushima import constants
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import MissingInputDataError
from artushima.commons.exceptions import InvalidInputDataError
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

    def test_new_user(self):
        """
        The test checks if the method correctly calls the corresponding repository.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "test_hash_1",
            "role": constants.ROLE_PLAYER
        }

        self.user_dao_mock.create.return_value = test_data_creator.create_test_user(1)

        # when
        user_internal_service.create_user(data)

        # then
        self.user_dao_mock.create.assert_called_once_with(data)

    def test_data_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the given input data is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(None)

    def test_user_name_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the user name is missing
        in the input data.
        """

        # given
        data = {
            "password_hash": "test_hash_1",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_user_name_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the user name given in the input
        data is None.
        """

        # given
        data = {
            "user_name": None,
            "password_hash": "test_hash_1",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_user_name_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the user name given in the input
        data is an empty string.
        """

        # given
        data = {
            "user_name": "",
            "password_hasn": "test_hash_1",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_password_hash_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the password hash is missing
        in the input data.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_password_hash_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the password hash given
        in the input data is None.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": None,
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_password_hash_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the password hash given
        in the input data is an empty string.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_role_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the role is missing in the input
        data.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "test_hash_1"
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_role_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the role given in the input data
        is None.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "test_hash_1",
            "role": None
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_role_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError, when the role given in the input data
        is an empty string.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "test_hash_1",
            "role": ""
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.create_user(data)

    def test_role_is_invalid(self):
        """
        The test checks if the method raises an instance of InvalidInputDataError, when the role given in the input data
        does not match any of the known roles.
        """

        # given
        data = {
            "user_name": "test_user_1",
            "password_hash": "test_hash_1",
            "role": "invalid_role"
        }

        # when then
        with self.assertRaises(InvalidInputDataError):
            user_internal_service.create_user(data)


class ReadUserByUserNameTest(_TestCaseWithMocks):
    """
    Tests for the method user_internal_service_test.read_user_by_user_name.
    """

    def test_read_user_successful(self):
        """
        The test checks if the method correctly calls the corresponding repository.
        """

        # given
        user = test_data_creator.create_test_user(1)
        self.user_dao_mock.read_by_user_name.return_value = user.map_to_dict()

        # when
        user_data = user_internal_service.read_user_by_user_name(user.user_name)

        # then
        self.assertIsNotNone(user_data)
        self.assertEqual(user.map_to_dict(), user_data)
        self.user_dao_mock.read_by_user_name.assert_called_once_with(user.user_name)

    def test_user_name_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given user name is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.read_user_by_user_name(None)

    def test_user_name_is_empty(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the given user name is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            user_internal_service.read_user_by_user_name("")
