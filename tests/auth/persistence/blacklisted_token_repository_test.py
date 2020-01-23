"""
The testing module for the blacklisted token repository.
"""

from unittest import TestCase

from artushima.auth.persistence import blacklisted_token_repository
from artushima.auth.persistence.model import BlacklistedTokenEntity
from artushima.core import db_access, properties
from artushima.core.exceptions import PersistenceError


class PersistTest(TestCase):

    def setUp(self):
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_persist_new_blacklisted_token(self):
        # given
        blacklisted_token = BlacklistedTokenEntity()
        blacklisted_token.token = "test-token"

        # when
        blacklisted_token_repository.persist(blacklisted_token)

        # then
        self.assertIn(blacklisted_token, self.session.query(BlacklistedTokenEntity).all())

    def test_should_raise_persistence_error_when_token_value_is_none(self):
        # given
        blacklisted_token = BlacklistedTokenEntity()

        # when then
        with self.assertRaises(PersistenceError):
            blacklisted_token_repository.persist(blacklisted_token)

    def test_should_raise_value_error_when_argument_is_of_wrong_type(self):
        # given
        blacklisted_token = str()

        # when then
        with self.assertRaises(ValueError):
            blacklisted_token_repository.persist(blacklisted_token)


class ReadByTokenTest(TestCase):

    def setUp(self):
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_get_token_by_token_value(self):
        # given
        blacklisted_token = BlacklistedTokenEntity()
        blacklisted_token.token = "test-token"

        self.session.add(blacklisted_token)
        self.session.flush()

        # when
        found_token = blacklisted_token_repository.read_by_token("test-token")

        # then
        self.assertIsNotNone(found_token)

    def test_should_get_none_when_token_does_not_exist(self):
        # when
        found_token = blacklisted_token_repository.read_by_token("test-token")

        # then
        self.assertIsNone(found_token)
