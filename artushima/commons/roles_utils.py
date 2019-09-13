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

# The string representation of all roles that exist
_roles_str = {
    constants.ROLE_ADMIN: "role_admin",
    constants.ROLE_GAME_MASTER: "role_game_master",
    constants.ROLE_PLAYER: "role_player"
}


def check_if_role_exists(role: int) -> bool:
    """
    Check if the given role int value corresponds to any existing role.

    Arguments:
        - role - the role int value to check

    Returns:
        True if the role exists, False otherwise
    """

    return role in _roles


def get_str_role(role: int) -> str:
    """
    Get the string representation of the role code.

    Arguments:
        - role - the role int value

    Returns:
        string role representation
    """

    if not check_if_role_exists(role):
        return None

    return _roles_str[role]
