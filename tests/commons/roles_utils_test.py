"""
The test module for the roles_utils module.
"""

import unittest

from artushima import constants
from artushima.commons import roles_utils


class CheckIfRoleExistsTest(unittest.TestCase):
    """
    Tests for the method roles_utils.check_if_role_exists.
    """

    def test_role_admin(self):
        """
        The test checks if the method returns True, when checking the admin role.
        """

        # when
        response = roles_utils.check_if_role_exists(constants.ROLE_ADMIN)

        # then
        self.assertTrue(response)

    def test_role_game_master(self):
        """
        The test checks if the method returns True, when checking the game master role.
        """

        # when
        response = roles_utils.check_if_role_exists(constants.ROLE_GAME_MASTER)

        # then
        self.assertTrue(response)

    def test_role_player(self):
        """
        The test checks if the method returns True, when checking the player role.
        """

        # when
        response = roles_utils.check_if_role_exists(constants.ROLE_PLAYER)

        # then
        self.assertTrue(response)

    def test_not_existing_role(self):
        """
        The test checks if the method returns False, when checking non existing roles.
        """

        # when
        response_1 = roles_utils.check_if_role_exists(-1)
        response_2 = roles_utils.check_if_role_exists(4)
        response_3 = roles_utils.check_if_role_exists(99)

        # then
        self.assertFalse(response_1)
        self.assertFalse(response_2)
        self.assertFalse(response_3)