"""
The service dealing with the tasks performed on the application startup.
"""

from artushima.core import properties
from artushima.user import user_service
from artushima.user.roles import ALL_ROLES


def superuser_exists():
    """
    Check if the superuser exists in the database.
    """

    return user_service.get_user_by_user_name("superuser") is not None


def create_superuser():
    """
    Create the superuser.
    """

    superuser_password = properties.get_superuser_password()

    if not superuser_password:
        raise RuntimeError("Property {} is missing!".format(properties.PROPERTY_SUPERUSER_PASSWORD))

    user_service.create_user("SYSTEM", "superuser", superuser_password, roles=ALL_ROLES)
