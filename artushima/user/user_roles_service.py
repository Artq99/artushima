"""
The module managing user roles.
"""

from artushima.core.exceptions import BusinessError
from artushima.core.utils.argument_validator import validate_str_arg
from artushima.user.persistence import user_repository


def get_user_roles(user_name):
    """
    Get all roles that the given user has.
    """

    validate_str_arg(user_name, "User name")

    user = user_repository.read_by_user_name(user_name)

    if not user:
        raise BusinessError(f"User {user_name} does not exist!")

    return [role.role_name for role in user.user_roles]
