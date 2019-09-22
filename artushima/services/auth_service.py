"""
The service providing methods for user to log in, log out and authenticate.
"""

import werkzeug

from artushima import constants
from artushima import messages
from artushima.commons import logger
from artushima.commons import properties
from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
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

    # TODO try ... except
    token = auth_internal_service.generate_token(user).decode()

    current_user = {
        "userName": user["user_name"],
        "role": user["role"],
        "token": token
    }

    return service_utils.create_response_success(currentUser=current_user)


@transactional_service_method
def log_out(token: str) -> dict:
    """
    Blacklist the given token.

    Arguments:
        - token - the token to be blacklisted

    Returns:
        a dictionary containing data of the blacklisted token
    """

    try:
        persisted_token = auth_internal_service.blacklist_token(token)
    except PersistenceError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(messages.PERSISTENCE_ERROR)

    return service_utils.create_response_success(token=persisted_token)


@transactional_service_method
def authenticate(token: str, required_roles: list) -> dict:
    """
    Authenticate the given token.

    Arguments:
        - token - the token to authenticate
        - required_roles - roles allowed to pass this authentication; if
                           an empty list is passed, the role validation
                           is skipped

    Returns:
        a service response
    """

    # authenticating the test bearer token, if enabled
    if token == constants.TEST_BEARER_TOKEN:
        if properties.get_test_bearer_enabled():
            return service_utils.create_response_success()
        else:
            return service_utils.create_response_failure(messages.AUTHENTICATION_FAILED)

    # decoding the token
    try:
        decoded_token = auth_internal_service.decode_token(token)
    except TokenExpirationError:
        return service_utils.create_response_failure(messages.TOKEN_EXPIRED)
    except TokenInvalidError:
        return service_utils.create_response_failure(messages.AUTHENTICATION_FAILED)

    # getting the user
    try:
        user = user_internal_service.read_user_by_user_name(decoded_token["sub"])
    except PersistenceError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure(messages.PERSISTENCE_ERROR)

    if user is None:
        return service_utils.create_response_failure(messages.AUTHENTICATION_FAILED)

    # checking required roles, if specified
    if (len(required_roles) > 0) and (user["role"] not in required_roles):
        return service_utils.create_response_failure(messages.ACCESS_DENIED)

    return service_utils.create_response_success()
