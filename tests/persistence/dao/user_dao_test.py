"""
The test module for the user_dao module.
"""

from sqlalchemy.exc import IntegrityError

from tests import abstracts
from tests import test_data_creator

from artushima import constants
from artushima.commons.exceptions import PersistenceError
from artushima.persistence.dao import user_dao


class CreateTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the method user_dao.create.
    """

    def test_new_user(self):
        """
        The test checks if the method persists new user and returns its data.
        """

        # given
        data = {
            "user_name": "test_user",
            "password_hash": "test_hash",
            "role": constants.ROLE_PLAYER
        }

        # when
        persisted_data = user_dao.create(data)

        # then
        self.assertIsNotNone(persisted_data)
        self.assertEqual(1, persisted_data["id"])
        self.assertEqual("test_user", persisted_data["user_name"])
        self.assertEqual("test_hash", persisted_data["password_hash"])
        self.assertEqual(constants.ROLE_PLAYER, persisted_data["role"])
        self.assertEqual(0, persisted_data["opt_lock"])

    def test_user_name_is_none(self):
        """
        The test checks if the method raises a PersistenceError when the value for the key 'user_name' is None.
        """

        # given
        data = {
            "user_name": None,
            "password_hash": "test_hash",
            "role": constants.ROLE_PLAYER
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)

    def test_password_hash_is_none(self):
        """
        The test checks if the method persists a new user without a password hash.
        """

        # given
        data = {
            "user_name": "test_user",
            "password_hash": None,
            "role": constants.ROLE_PLAYER
        }

        # when
        persisted_data = user_dao.create(data)

        # then
        self.assertIsNotNone(persisted_data)
        self.assertEqual(None, persisted_data["password_hash"])

    def test_role_is_none(self):
        """
        The test checks if the method raises a PersistenceError when the value for the key 'role' is None.
        """

        # given
        data = {
            "user_name": "test_user",
            "password_hash": "test_hash",
            "role": None
        }

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            user_dao.create(data)

        self.assertEqual(
            "Error on persisting data. (artushima.persistence.dao.user_dao.create)",
            ctx.exception.message
        )
        self.assertIsInstance(ctx.exception.__cause__, IntegrityError)


class ReadByUsernameTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the mehtod user_dao.read_by_username.
    """

    def test_read_data(self):
        """
        The test checks if the method returns correct data.
        """

        # given
        test_user = test_data_creator.create_test_user(1234, "test_user")

        self.session.add(test_user)
        self.session.commit()

        # when
        found_user = user_dao.read_by_user_name("test_user")

        # then
        self.assertIsNotNone(found_user)
        self.assertEqual(1234, found_user["id"])
        self.assertEqual("test_user", found_user["user_name"])

    def test_user_does_not_exist(self):
        """
        The test checks if the method returns None, when there is no user of the given user name.
        """

        # when
        found_user = user_dao.read_by_user_name("non_existing_user")

        # then
        self.assertIsNone(found_user)
