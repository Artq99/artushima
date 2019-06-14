"""
The test module for the user_dao module.
"""

from tests import abstracts
from tests import persistence_tests_util

from artushima.persistence.dao import user_dao


class ReadByUsernameTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the mehtod user_dao.read_by_username.
    """

    def test_read_data(self):
        """
        The test checks if the method returns correct data.
        """

        # given
        test_user = persistence_tests_util.create_test_user(1234, "test_user")

        self.session.add(test_user)
        self.session.commit()

        # when
        found_user = user_dao.read_by_user_name("test_user")

        # then
        self.assertIsNotNone(found_user)
        self.assertEqual(1234, found_user["id"])
        self.assertEqual("test_user", found_user["username"])

    def test_user_does_not_exist(self):
        """
        The test checks if the method returns None, when there is no user of the given username.
        """

        # when
        found_user = user_dao.read_by_user_name("non_existing_user")

        # then
        self.assertIsNone(found_user)
