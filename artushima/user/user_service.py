"""
The service for management of users.
"""

from datetime import datetime

from werkzeug import security

from artushima.core.exceptions import BusinessError
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import (UserEntity, UserHistoryEntity,
                                              UserRoleEntity)


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


def create_user(editor_name, user_name, password, roles=None):
    """
    Create a new user with the given name and password, granting him/her the given roles.
    """

    _check_arg_password(password)

    if user_repository.read_by_user_name(user_name) is not None:
        raise BusinessError("User {} already exists!".format(user_name))

    timestamp = datetime.now()
    user = _create_user_entity(user_name, password, timestamp)
    _grant_roles(user, roles, timestamp)
    _create_and_assing_history_entry_creation(user, editor_name, timestamp)

    user_repository.persist(user)


def _check_arg_password(password):
    if password is None:
        raise BusinessError("Password must be provided!")

    if not isinstance(password, str):
        raise ValueError("Password must be a string value!")

    if not password:
        raise BusinessError("Password must be provided!")


def _create_user_entity(user_name, password, timestamp):
    user = UserEntity()
    user.user_name = user_name
    user.password_hash = security.generate_password_hash(password)
    user.created_on = timestamp
    user.modified_on = timestamp
    user.opt_lock = 0

    return user


def _grant_roles(user, roles, timestamp):
    if roles is not None:
        for role_name in roles:
            role = UserRoleEntity()
            role.created_on = timestamp
            role.modified_on = timestamp
            role.opt_lock = 0
            role.role_name = role_name
            role.user = user


def _create_and_assing_history_entry_creation(user, editor_name, timestamp):
    user_history_entry = UserHistoryEntity()
    user_history_entry.created_on = timestamp
    user_history_entry.modified_on = timestamp
    user_history_entry.opt_lock = 0
    user_history_entry.editor_name = editor_name
    user_history_entry.message = "Użytkownik {} został utworzony.".format(user.user_name)
    user_history_entry.user = user
