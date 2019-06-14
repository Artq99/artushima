"""
The internal service dealing with data of the user entity.
"""

from artushima.commons.exceptions import BusinessError
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
