"""
The module containing utilities for managing user roles.
"""

from artushima import constants


# The list of all roles that exist
_roles = [
    constants.ROLE_ADMIN,
    constants.ROLE_GAME_MASTER,
    constants.ROLE_PLAYER
]


def check_if_role_exists(role: str) -> bool:
    """
    Check if the given role int value corresponds to any existing role.

    Arguments:
        - role - the role to check

    Returns:
        True if the role exists, False otherwise
    """

    return role in _roles
