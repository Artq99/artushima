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


def create_test_user_history(id: int, user_id: int, editor_name: str = "TEST") -> model.UserHistoryEntity:
    """
    Create an instance of the user history entity.

    The method requires an ID for the new entity and the ID of the user. The name of the editor, if not specified, is
    set to the default 'TEST'. The rest of the fields are set to the following default values:
        - message is set to 'Test message <ID>.'
        - created_on is set to the current date and time
        - modified_on is set to the current date and time
        - opt_lock is set to 0

    Arguments:
        - id - the ID for the newly created test entity
        - user_id - the ID of the user for whom the entry is created
        - editor_name - the name of the subject that caused the change (optional)

    Returns:
        an instance of the UserHistoryEntity class
    """

    user_history = model.UserHistoryEntity()
    user_history.id = id
    user_history.user_id = user_id
    user_history.editor_name = editor_name
    user_history.message = "Test message {}.".format(user_history.id)
    user_history.created_on = datetime.now()
    user_history.modified_on = datetime.now()
    user_history.opt_lock = 0

    return user_history


def create_test_blacklisted_token(id: int) -> model.BlacklistedTokenEntity:
    """
    Create an instance of the blacklisted token entity.

    The atribute 'token' is set to 'token_<id>'.

    Arguments:
        - id - the ID of the new blacklisted token

    Returns:
        an instance of the BlacklistedTokenEntity class
    """

    blacklisted_token = model.BlacklistedTokenEntity()
    blacklisted_token.id = id
    blacklisted_token.token = "token_{}".format(blacklisted_token.id)

    return blacklisted_token
