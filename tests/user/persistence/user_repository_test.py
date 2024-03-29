"""
The testing module for the user repository.
"""

from datetime import datetime
from unittest import TestCase

from artushima.core import db_access, properties
from artushima.core.exceptions import PersistenceError
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import (UserEntity, UserHistoryEntity,
                                              UserRoleEntity)
from tests import assertModelInitialized


class PersistTest(TestCase):

    def setUp(self):
        assertModelInitialized()
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_persist_new_user(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        # when
        user_repository.persist(user)

        # then
        self.assertIn(user, self.session.query(UserEntity).all())

    def test_should_persist_new_user_with_history_entry(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        user_history_entry = UserHistoryEntity()
        user_history_entry.created_on = datetime.utcnow()
        user_history_entry.modified_on = datetime.utcnow()
        user_history_entry.opt_lock = 0
        user_history_entry.editor_name = "test"
        user_history_entry.message = "test message"
        user_history_entry.user = user

        # when
        user_repository.persist(user)

        # then
        self.assertIsNotNone(self.session.query(UserEntity).filter_by(user_name="test_user").first())
        self.assertIsNotNone(self.session.query(UserHistoryEntity).filter_by(user=user).first())

    def test_should_persist_new_user_with_role(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        user_role = UserRoleEntity()
        user_role.created_on = datetime.utcnow()
        user_role.modified_on = datetime.utcnow()
        user_role.opt_lock = 0
        user_role.role_name = "test_role"
        user_role.user = user

        # when
        user_repository.persist(user)

        # then
        self.assertIsNotNone(self.session.query(UserEntity).filter_by(user_name="test_user").first())
        self.assertIsNotNone(self.session.query(UserRoleEntity).filter_by(user=user).first)

    def test_should_update_user(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        user.password_hash = "test_hash"
        user_repository.persist(user)

        # then
        self.assertEqual(
            "test_hash",
            self.session.query(UserEntity).filter_by(user_name="test_user").first().password_hash
        )

    def test_should_raise_persistence_error_on_constraint_violation(self):
        # given
        user = UserEntity()

        # when then
        with self.assertRaises(PersistenceError):
            user_repository.persist(user)

    def test_should_raise_value_error_when_argument_is_of_wrong_type(self):
        # given
        user = str()

        # when then
        with self.assertRaises(ValueError):
            user_repository.persist(user)


class ReadByIdTest(TestCase):

    def setUp(self):
        assertModelInitialized()
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_get_user_by_id(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        found_user = user_repository.read_by_id(user.id)

        # then
        self.assertIsNotNone(found_user)
        self.assertEqual(user, found_user)

    def test_should_get_none_when_user_does_not_exist(self):
        # when
        found_user = user_repository.read_by_id(9999)

        # then
        self.assertIsNone(found_user)


class ReadByUserNameTest(TestCase):

    def setUp(self):
        assertModelInitialized()
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_get_user_by_user_name(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        found_user = user_repository.read_by_user_name("test_user")

        # then
        self.assertIsNotNone(found_user)
        self.assertEqual(user, found_user)

    def test_should_get_none_when_user_does_not_exist(self):
        # when
        found_user = user_repository.read_by_user_name("test_user")

        # then
        self.assertIsNone(found_user)


class ReadAllTest(TestCase):

    def setUp(self):
        assertModelInitialized()
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_read_all_users(self):
        # given
        user_1 = UserEntity()
        user_1.user_name = "test_user_1"
        user_1.created_on = datetime.utcnow()
        user_1.modified_on = datetime.utcnow()
        user_1.opt_lock = 0

        user_2 = UserEntity()
        user_2.user_name = "test_user_2"
        user_2.created_on = datetime.utcnow()
        user_2.modified_on = datetime.utcnow()
        user_2.opt_lock = 0

        self.session.add(user_1)
        self.session.add(user_2)
        self.session.flush()

        # when
        found_users = user_repository.read_all()

        # then
        self.assertIsNotNone(found_users)
        self.assertIn(user_1, found_users)
        self.assertIn(user_2, found_users)
