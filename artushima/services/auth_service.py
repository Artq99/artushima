"""
The service providing methods for user to log in, log out and authenticate.
"""

from artushima import constants
from artushima import messages
from artushima.commons import properties
from artushima.commons import error_handler
from artushima.commons.exceptions import ArtushimaError
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

    try:
        user = user_internal_service.read_user_by_user_name(user_name)

        if (user is None) or (not auth_internal_service.check_password(password, user["password_hash"])):
            return service_utils.create_response_failure(messages.LOGIN_ERROR)

        token = auth_internal_service.generate_token(user)

        return service_utils.create_response_success(currentUser=_create_current_user_data(user, token))

    except ArtushimaError as e:
        return service_utils.create_response_failure(error_handler.handle(e))


def _create_current_user_data(user: dict, token: bytes):

    return {
        "userName": user["user_name"],
        "role": user["role"],
        "token": token.decode()
    }


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

        return service_utils.create_response_success(token=persisted_token)

    except ArtushimaError as e:
        return service_utils.create_response_failure(error_handler.handle(e))


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

    try:
        if auth_internal_service.check_if_token_is_blacklisted(token):
            return service_utils.create_response_failure(messages.AUTHENTICATION_FAILED)

        decoded_token = auth_internal_service.decode_token(token)
        user = user_internal_service.read_user_by_user_name(decoded_token["sub"])

        if user is None:
            return service_utils.create_response_failure(messages.AUTHENTICATION_FAILED)

        if (len(required_roles) > 0) and (user["role"] not in required_roles):
            return service_utils.create_response_failure(messages.ACCESS_DENIED)

        return service_utils.create_response_success()

    except ArtushimaError as e:
        return service_utils.create_response_failure(error_handler.handle(e))
