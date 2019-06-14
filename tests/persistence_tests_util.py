"""
The module containing utilities for persistence tests.
"""

from datetime import datetime

from artushima import constants
from artushima.persistence import model


def create_test_user(id: int, user_name: str, role=constants.ROLE_PLAYER):
    """
    Create an instance of the user entity.

    The method requires only the ID and the user name. Role definition is optional. The rest of the fields are
    initialised with default values.

    Arguments:
        - id - the ID of the new user
        - user_name - the user name of the new user
        - role - the role of the new user (optional)

    Returns:
        an instance of the UserEntity class
    """

    user = model.UserEntity()
    user.id = id
    user.user_name = user_name
    user.role = role
    user.created_on = datetime.now()
    user.modified_on = datetime.now()
    user.opt_lock = 0

    return user
