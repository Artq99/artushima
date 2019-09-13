"""
The test module for the blacklisted_token_dao module.
"""

from tests import abstracts

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
