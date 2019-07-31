"""
The service providing methods used on application startup.
"""

from werkzeug import security

from artushima import constants
from artushima.commons import logger
from artushima.commons import properties
from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.persistence.decorators import transactional_service_method
from artushima.internal_services import user_internal_service
from artushima.internal_services import user_history_internal_service
from artushima.services import service_utils


@transactional_service_method
def check_if_superuser_exists():
    """
    Check if the superuser exists.

    Returns:
        a service response containing the 'superuser_exists' key set to True or False, provided no error has
        occured.
    """

    try:
        superuser_exists = user_internal_service.check_if_user_exists("superuser")
    except PersistenceError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Błąd odczytu danych.")
    except BusinessError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Błąd aplikacji.")

    return service_utils.create_response_success(superuser_exists=superuser_exists)


@transactional_service_method
def create_superuser():
    """
    Creates the superuser.

    Returns:
        a standard service response with no particular data.
    """

    superuser_password = properties.get_superuser_password()

    if superuser_password is None:
        return service_utils.create_response_failure("Brakujące dane: hasło dla superużytkownika.")

    password_hash = security.generate_password_hash(superuser_password)

    user_data = {
        "user_name": "superuser",
        "password_hash": password_hash,
        "role": constants.ROLE_ADMIN
    }

    try:
        user = user_internal_service.create_user(user_data)
    except (PersistenceError, BusinessError) as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Superużytkownik nie mógł zostać utworzony.")

    user_history_data = {
        "editor_name": "System",
        "message": "Superużytkownik został utworzony.",
        "user_id": user["id"]
    }

    try:
        user_history_internal_service.create_user_history_entry(user_history_data)
    except (PersistenceError, BusinessError) as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Wpis do historii dla superużytkownika nie mógł zostać utworzony.")

    return service_utils.create_response_success()
