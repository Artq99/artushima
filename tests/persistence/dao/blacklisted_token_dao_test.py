"""
The test module for the blacklisted_token_dao module.
"""

from tests import abstracts

from artushima.persistence import model
from artushima.commons.exceptions import PersistenceError
from artushima.persistence.dao import blacklisted_token_dao


class CreateTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the method blacklisted_token_dao.create.
    """

    def test_new_blacklisted_token(self):
        """
        The test checks if the method persists a new blacklisted token and returns its data.
        """

        # given
        token = "test_token"

        # when
        persisted_data = blacklisted_token_dao.create(token)

        # then
        self.assertIsNotNone(persisted_data)
        self.assertEqual(1, persisted_data["id"])
        self.assertEqual("test_token", persisted_data["token"])

    def test_token_is_none(self):
        """
        The test checks if the method raises a PersistenceError when the given token is None.
        """

        # when then
        with self.assertRaises(PersistenceError) as ctx:
            blacklisted_token_dao.create(None)

        self.assertEqual(
            "The argument 'token' cannot be None. (artushima.persistence.dao.blacklisted_token_dao.create)",
            ctx.exception.message
        )


class ReadByTokenTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the method blacklisted_token_dao.read_by_token.
    """

    def test_read_blacklisted_token(self):
        """
        The test checks if the method can read a blacklisted token entity and return its data by the given token.
        """

        # given
        token = "test_token"
        token_entity = model.BlacklistedTokenEntity()
        token_entity.token = token

        self.session.add(token_entity)
        self.session.flush()

        # when
        token_data = blacklisted_token_dao.read_by_token(token)

        # then
        self.assertEqual(token_entity.id, token_data["id"])
        self.assertEqual(token, token_data["token"])

    def test_token_not_in_database(self):
        """
        The test checks if the method returns None if the token has not been blacklisted.
        """

        # given
        token = "test_token"

        # when
        token_data = blacklisted_token_dao.read_by_token(token)

        # then
        self.assertIsNone(token_data)
