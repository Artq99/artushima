"""
The service providing methods used on application startup.
"""

from werkzeug import security

from artushima import constants
from artushima import messages
from artushima.commons import logger
from artushima.commons import properties
from artushima.commons import error_handler
from artushima.commons.exceptions import ArtushimaError
from artushima.commons.exceptions import MissingApplicationPropertyError
from artushima.persistence.decorators import transactional_service_method
from artushima.internal_services import user_internal_service
from artushima.internal_services import user_history_internal_service
from artushima.services import service_utils


_PROPERTY_SUPERUSER_PASSWORD: str = "superuser_password"
_SUPERUSER: str = "superuser"
_SYSTEM: str = "System"


@transactional_service_method
def check_if_superuser_exists() -> dict:
    """
    Check if the superuser exists.

    Returns:
        a service response containing the 'superuser_exists' key set to True or False, provided no error has
        occured.
    """

    try:
        superuser_exists = user_internal_service.check_if_user_exists("superuser")
    except ArtushimaError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(error_handler.handle(e))

    return service_utils.create_response_success(superuser_exists=superuser_exists)


@transactional_service_method
def create_superuser() -> dict:
    """
    Create the superuser.

    Returns:
        a standard service response with the status 'SUCCESS".
    """

    try:
        superuser_password: str = _get_superuser_password()
        password_hash: str = security.generate_password_hash(superuser_password)

        superuser_data = _create_superuser_data(password_hash)
        user: dict = user_internal_service.create_user(superuser_data)

        user_history_data = _create_superuser_history_data(user)
        user_history_internal_service.create_user_history_entry(user_history_data)

        return service_utils.create_response_success()

    except ArtushimaError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(error_handler.handle(e))


def _get_superuser_password() -> str:

    superuser_password: str = properties.get_superuser_password()

    if superuser_password is None or len(superuser_password) == 0:
        raise MissingApplicationPropertyError(_PROPERTY_SUPERUSER_PASSWORD, __name__, create_superuser.__name__)

    return superuser_password


def _create_superuser_data(password_hash: str) -> dict:

    return {
        "user_name": _SUPERUSER,
        "password_hash": password_hash,
        "role": constants.ROLE_ADMIN
    }


def _create_superuser_history_data(superuser: dict) -> dict:

    return {
        "editor_name": _SYSTEM,
        "message": messages.DBMSG_SUPERUSER_CREATED,
        "user_id": superuser["id"]
    }
