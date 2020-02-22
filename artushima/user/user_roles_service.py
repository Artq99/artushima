"""
The module managing user roles.
"""

from datetime import datetime

from artushima.core.exceptions import BusinessError
from artushima.core.utils.argument_validator import (validate_list_arg,
                                                     validate_str_arg)
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import UserHistoryEntity, UserRoleEntity


def get_user_roles(user_name):
    """
    Get all roles that the given user has.
    """

    validate_str_arg(user_name, "User name")

    user = user_repository.read_by_user_name(user_name)

    if not user:
        raise BusinessError(f"User {user_name} does not exist!")

    return [role.role_name for role in user.user_roles]


def grant_roles(editor_name, user_name, roles):
    """
    Grant the roles to the given user.
    """

    validate_str_arg(editor_name, "Editor name")
    validate_str_arg(user_name, "User name")
    validate_list_arg(roles, "Roles")

    user = user_repository.read_by_user_name(user_name)

    if not user:
        raise BusinessError(f"User {user_name} does not exist!")

    previous_user_roles = [role.role_name for role in user.user_roles]

    timestamp = datetime.now()

    for role in roles:
        if role not in previous_user_roles:
            new_role = UserRoleEntity()
            new_role.created_on = timestamp
            new_role.modified_on = timestamp
            new_role.opt_lock = 0
            new_role.role_name = role
            new_role.user = user

            user_history_entry = UserHistoryEntity()
            user_history_entry.created_on = timestamp
            user_history_entry.modified_on = timestamp
            user_history_entry.opt_lock = 0
            user_history_entry.editor_name = editor_name
            user_history_entry.message = f"Przyznano rolę '{role}'."
            user_history_entry.user = user

    user_repository.persist(user)
