"""
The internal service dealing with data of the user entity.
"""

from artushima.commons import roles_utils
from artushima.commons.exceptions import MissingInputDataError
from artushima.commons.exceptions import InvalidInputDataError
from artushima.persistence.dao import user_dao


_ARG_DATA = "data"
_ARG_USER_NAME = "user_name"
_ARG_PASSWORD_HASH = "password_hash"
_ARG_ROLE = "role"


def check_if_user_exists(user_name: str) -> bool:
    """
    Check if a user of the given name exists.

    Arguments:
        - user_name - the name of the user to check

    Returns:
        True if the user exists, False otherwise
    """

    if user_name is None:
        raise MissingInputDataError(_ARG_USER_NAME, __name__, check_if_user_exists.__name__)

    user = user_dao.read_by_user_name(user_name)

    return user is not None


def create_user(data: dict) -> dict:
    """
    Create a new user.

    Arguments:
        - data - the dictionary containing the following entries:
            - user_name
            - password_hash
            - role

    Returns:
        a dictionary containing data of the newly created user
    """

    _check_input_data_for_create_user(data)

    return user_dao.create(data)


def _check_input_data_for_create_user(data: dict) -> None:

    if data is None:
        raise MissingInputDataError(_ARG_DATA, __name__, create_user.__name__)

    if (_ARG_USER_NAME not in data.keys()) or (not data[_ARG_USER_NAME]):
        raise MissingInputDataError(_ARG_USER_NAME, __name__, create_user.__name__)

    if (_ARG_PASSWORD_HASH not in data.keys()) or (not data[_ARG_PASSWORD_HASH]):
        raise MissingInputDataError(_ARG_PASSWORD_HASH, __name__, create_user.__name__)

    if (_ARG_ROLE not in data.keys()) or (not data[_ARG_ROLE]):
        raise MissingInputDataError(_ARG_ROLE, __name__, create_user.__name__)

    if not roles_utils.check_if_role_exists(data[_ARG_ROLE]):
        raise InvalidInputDataError(_ARG_ROLE, __name__, create_user.__name__)


def read_user_by_user_name(user_name: str) -> dict:
    """
    Read the user by its user name.

    Arguments:
        - user_name - the user name

    Returns:
        a dictionary containing data of the user, if it could be found, None otherwise
    """

    if not user_name:
        raise MissingInputDataError(_ARG_USER_NAME, __name__, read_user_by_user_name.__name__)

    return user_dao.read_by_user_name(user_name)
