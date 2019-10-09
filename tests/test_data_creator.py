"""
The module containing methods for creating test data.
"""

from datetime import datetime

from artushima import constants
from artushima.persistence import model


def create_test_user(id: int, user_name: str = None, role: str = constants.ROLE_PLAYER) -> model.UserEntity:
    """
    Create an instance of the user entity.

    The method requires only the ID. User name and role definition are optional. The rest of the fields are
    initialised with default values:
        - user_name, if not specified, is set to 'test_user_<id>'
        - role, if not specified, is set to ROLE_USER
        - password_hash is set to 'test_hash_<id>'
        - created_on is set to the current date and time
        - modified_on is set to the current date and time
        - opt_lock is set to 0

    Arguments:
        - id - the ID of the new user
        - user_name - the user name of the new user (optional)
        - role - the role of the new user (optional)

    Returns:
        an instance of the UserEntity class
    """

    if user_name is None:
        user_name = "test_user_{}".format(id)

    user = model.UserEntity()
    user.id = id
    user.user_name = user_name
    user.password_hash = "test_hash_{}".format(id)
    user.role = role
    user.created_on = datetime.now()
    user.modified_on = datetime.now()
    user.opt_lock = 0

    return user
