"""
The service dealing with the tasks performed on the application startup.
"""

from artushima.user import user_service


def superuser_exists():
    """
    Check if the superuser exists in the database.
    """

    return user_service.get_user_by_user_name("superuser") is not None
