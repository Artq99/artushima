"""
The service providing methods for user to log in, log out and authenticate.
"""

import werkzeug

from artushima import messages
from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons import logger
from artushima.commons import roles_utils
from artushima.persistence.decorators import transactional_service_method
from artushima.internal_services import user_internal_service
from artushima.internal_services import auth_internal_service
from artushima.services import service_utils


@transactional_service_method
def log_in(user_name: str, password: str) -> dict:
    """
    Get the authentication token.

    Arguments:
        - user_name - the login
        - password - the password

    Returns:
        a service response containing the authentication token.
    """

    if not user_name:
        return service_utils.create_response_failure(messages.USERNAME_MISSING)

    if not password:
        return service_utils.create_response_failure(messages.PASSWORD_MISSING)

    try:
        user = user_internal_service.read_user_by_user_name(user_name)
    except PersistenceError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(messages.PERSISTENCE_ERROR)
    except BusinessError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(messages.APPLICATION_ERROR)

    if user is None:
        return service_utils.create_response_failure(messages.LOGIN_ERROR)

    if not werkzeug.check_password_hash(user["password_hash"], password):
        return service_utils.create_response_failure(messages.LOGIN_ERROR)

    token = auth_internal_service.generate_token(user).decode()

    current_user = {
        "userName": user["user_name"],
        "role": roles_utils.get_str_role(user["role"]),
        "token": token
    }

    return service_utils.create_response_success(currentUser=current_user)
