"""
The internal service dealing with data of the user entity.
"""

from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import MissingInputDataError
from artushima.persistence.dao import user_dao


def check_if_user_exists(user_name: str):
    """
    Check if a user of the given name exists.

    Arguments:
        - user_name - the name of the user to check

    Returns:
        True if the user exists, False otherwise
    """

    if user_name is None:
        raise BusinessError(
            "The argument 'user_name' cannot be None.", __name__, check_if_user_exists.__name__
        )

    user = user_dao.read_by_user_name(user_name)

    return user is not None


def create_user(data: dict):
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

    return user_dao.create(data)


def read_user_by_user_name(user_name: str) -> dict:
    """
    Read the user by its user name.

    Arguments:
        - user_name - the user name

    Returns:
        a dictionary containing data of the user, if it could be found, None otherwise
    """

    if not user_name:
        raise MissingInputDataError("user_name", __name__, read_user_by_user_name.__name__)

    return user_dao.read_by_user_name(user_name)
