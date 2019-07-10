"""
The service providing methods used on application startup.
"""

from artushima.commons import logger
from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.persistence.decorators import transactional_service_method
from artushima.internal_services import user_internal_service
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
