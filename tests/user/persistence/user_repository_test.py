"""
The testing module for the user repository.
"""

from datetime import datetime
from unittest import TestCase

from artushima.core import db_access, properties
from artushima.core.exceptions import PersistenceError
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import UserEntity


class PersistTest(TestCase):

    def setUp(self):
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
        user.created_on = datetime.now()
        user.modified_on = datetime.now()
        user.opt_lock = 0

        # when
        user_repository.persist(user)

        # then
        self.assertEqual(1, self.session.query(UserEntity).count())

    def test_should_update_user(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.now()
        user.modified_on = datetime.now()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        user.password_hash = "test_hash"
        user_repository.persist(user)

        # then
        self.assertEqual("test_hash", self.session.query(UserEntity).first().password_hash)

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


class ReadByUserNameTest(TestCase):

    def setUp(self):
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
        user.created_on = datetime.now()
        user.modified_on = datetime.now()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        found_user = user_repository.read_by_user_name("test_user")

        # then
        self.assertIsNotNone(found_user)
        self.assertEqual(user, found_user)

    def test_should_get_null_when_user_does_not_exist(self):
        # when
        found_user = user_repository.read_by_user_name("test_user")

        # then
        self.assertIsNone(found_user)
