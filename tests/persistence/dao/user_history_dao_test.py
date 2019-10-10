"""
The test module for the user_history_dao module.
"""

from sqlalchemy.exc import IntegrityError

from tests import abstracts
from tests import test_data_creator

from artushima.commons.exceptions import PersistenceError
from artushima.persistence import model
from artushima.persistence.dao import user_history_dao


class CreateTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the method user_history_dao.create.
    """

    def test_new_entry(self):
        """
        The test checks if the method creates a new history entry.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": "test_editor",
            "message": "test message",
            "user_id": user.id
        }

        # when
        entry = user_history_dao.create(data)

        # then
        self.assertIsNotNone(entry)
        self.assertEqual("test_editor", entry["editor_name"])
        self.assertEqual("test message", entry["message"])
        self.assertEqual(user.id, entry["user_id"])

        entries = self.session.query(model.UserHistoryEntity).all()
        self.assertEqual(1, len(entries))

    def test_editor_name_is_none(self):
        """
        The test checks if a PersistenceError is raised when the entry 'editor_name' is None.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": None,
            "message": "test message",
            "user_id": user.id
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)

    def test_editor_name_is_missing(self):
        """
        The test checks if a PersistenceError is raised when the entry 'editor_name' is missing.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "message": "test message",
            "user_id": user.id
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "The argument 'editor_name' is missing. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )

    def test_message_is_none(self):
        """
        The test checks if a PersistenceError is raised when the argument 'message' is None."
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": "test_editor",
            "message": None,
            "user_id": user.id
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)

    def test_message_is_missing(self):
        """
        The test checks if a PersistenceError is raised when the argument 'message' is missing.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": "test_editor",
            "user_id": user.id
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEquals(
            "The argument 'message' is missing. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )

    def test_user_id_is_none(self):
        """
        The test checks if a PersistenceError is raised when the argument 'user_id' is None.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": "test_editor",
            "message": "test message",
            "user_id": None
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)

    def test_user_id_is_missing(self):
        """
        The test checks if a PersistenceError is raised when the argument 'user_id' is missing.
        """

        # given
        user = test_data_creator.create_test_user(1, "test_user")
        self.session.add(user)
        self.session.flush()

        data = {
            "editor_name": "test_editor",
            "message": "test message",
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "The argument 'user_id' is missing. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )

    def test_user_does_not_exists(self):
        """
        The test checks if a PersistenceError is raised when the given ID of a user points to no existing user.
        """

        # given
        data = {
            "editor_name": "test_editor",
            "message": "test message",
            "user_id": 9999
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_history_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_history_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)
