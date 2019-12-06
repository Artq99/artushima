"""
The service for management of users.
"""

from artushima.core.exceptions import BusinessError
from artushima.user.persistence import user_repository


def get_user_by_user_name(name):
    """
    Get the user data by his/her user name.
    """

    _check_arg_name(name)

    user = user_repository.read_by_user_name(name)

    if user is None:
        return None

    return _map_user_entity_to_dict(user)


def _check_arg_name(name):
    if name is None:
        raise BusinessError("Name must be provided!")

    if not isinstance(name, str):
        raise ValueError("Name must be a string value!")

    if not name:
        raise BusinessError("Name must be provided!")


def _map_user_entity_to_dict(user):
    return {
        "id": user.id,
        "user_name": user.user_name,
        "created_on": user.created_on,
        "modified_on": user.modified_on,
        "opt_lock": user.opt_lock,
        "password_hash": user.password_hash
    }
