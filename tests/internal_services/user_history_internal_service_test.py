"""
The test module for the user_history_internal_service module.
"""

from unittest import mock
from tests import abstracts

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

    def test_positive_output(self):
        """
        The test checks if the method calls correctly the corresponding repository.
        """

        # given
        data = {
            "editor_name": "test_editor",
            "message": "test message",
            "user_id": 1
        }

        dao_return_value = {
            "id": 1,
            "editor_name": "test_editor",
            "message": "test message",
            "user_id": 1
        }

        self.user_history_dao_mock.create.return_value = dao_return_value

        # when
        response = user_history_internal_service.create_user_history_entry(data)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(dao_return_value, response)
        self.user_history_dao_mock.create.assert_called_once_with(data)
