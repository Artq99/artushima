"""
The test module for the user_history_internal_service module.
"""

from unittest import mock

from tests import abstracts
from tests import test_data_creator

from artushima.commons.exceptions import MissingInputDataError
from artushima.persistence.dao import user_history_dao
from artushima.internal_services import user_history_internal_service


class CreateUserHistoryEntryTest(abstracts.AbstractServiceTestClass):
    """
    Tests for the method user_history_internal_service.create_user_history_entry.
    """

    def setUp(self):
        super().setUp()

        self.user_history_dao_mock = mock.create_autospec(user_history_dao)
        user_history_internal_service.user_history_dao = self.user_history_dao_mock

    def tearDown(self):
        super().tearDown()

        user_history_internal_service.user_history_dao = user_history_dao

    def test_new_entry(self):
        """
        The test checks if the method can process the input data and call the DAO.
        """

        # given
        data = {
            "editor_name": "TEST",
            "message": "Test message 1",
            "user_id": 1
        }

        persisted_entry = test_data_creator.create_test_user_history(1, 1)

        self.user_history_dao_mock.create.return_value = persisted_entry.map_to_dict()

        # when
        response = user_history_internal_service.create_user_history_entry(data)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(persisted_entry.map_to_dict(), response)
        self.user_history_dao_mock.create.assert_called_once_with(data)

    def test_data_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the argument 'data' is None.
        """

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(None)

    def test_editor_name_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the editor name is missing in
        the input data.
        """

        # given
        data = {
            "message": "Test message 1.",
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_editor_name_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the editor name given in
        the input data is None.
        """

        # given
        data = {
            "editor_name": None,
            "message": "Test message 1.",
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_editor_name_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the editor name given in
        the input data is an empty string.
        """

        # given
        data = {
            "editor_name": "",
            "message": "Test message 1.",
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_message_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the message is missing in
        the input data.
        """

        # given
        data = {
            "editor_name": "TEST",
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_message_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the message given in the input
        data is None.
        """

        # given
        data = {
            "editor_name": "TEST",
            "message": None,
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_message_is_empty_string(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the message given in the input
        data is an empty string.
        """

        # given
        data = {
            "editor_name": "TEST",
            "message": "",
            "user_id": 1
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_user_id_is_missing(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the user ID is missing in
        the input data.
        """

        # given
        data = {
            "editor_name": "TEST",
            "message": "Test message 1."
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)

    def test_user_is_is_none(self):
        """
        The test checks if the method raises an instance of MissingInputDataError when the user id given in the input
        data is None.
        """

        # given
        data = {
            "editor_name": "TEST",
            "message": "Test message 1.",
            "user_id": None
        }

        # when then
        with self.assertRaises(MissingInputDataError):
            user_history_internal_service.create_user_history_entry(data)
