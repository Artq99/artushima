"""
The module dealing with user authenication.
"""

from datetime import datetime, timedelta

import jwt
import werkzeug
from jwt import InvalidTokenError

from artushima.auth.persistence import blacklisted_token_repository
from artushima.auth.persistence.model import BlacklistedTokenEntity
from artushima.core import properties
from artushima.core.exceptions import BusinessError
from artushima.core.properties import (PROPERTY_TEST_BEARER_ENABLED,
                                       PROPERTY_TOKEN_EXPIRATION_TIME)
from artushima.user import user_roles_service, user_service

TEST_BEARER_TOKEN = "test-9999"


def log_in(user_name, password):
    """
    Authenticate the user and return the current user data with authentication token.
    """

    user = user_service.get_user_by_user_name(user_name)

    if user is None:
        raise BusinessError(f"User {user_name} does not exist!")

    if not werkzeug.check_password_hash(user["password_hash"], password):
        raise BusinessError(f"Incorrect password!")

    payload = _create_jwt_payload(user_name)
    token = jwt.encode(payload, properties.get_app_secret_key(), algorithm="HS256")
    user_roles = user_roles_service.get_user_roles(user_name)

    return _create_log_in_response(user_name, user_roles, token)


def _create_jwt_payload(user_name):
    timestamp = datetime.utcnow()
    exp_time = _get_and_validate_exp_time()

    return {
        "sub": user_name,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=exp_time)
    }


def _get_and_validate_exp_time():
    exp_time = properties.get_token_expiration_time()

    if not exp_time:
        raise BusinessError(f"Property {PROPERTY_TOKEN_EXPIRATION_TIME} missing!")

    return int(exp_time)


def _create_log_in_response(user_name, user_roles, token):
    return {
        "user_name": user_name,
        "roles": user_roles,
        "token": token.decode()
    }


def is_token_ok(token):
    """
    Authenticate the token.
    """

    if token is None:
        return False

    token = token.split(" ")[1]

    if token == TEST_BEARER_TOKEN:
        if _is_test_bearer_enabled():
            return True
        else:
            return False

    if _is_token_blacklisted(token):
        return False

    try:
        decoded_token = jwt.decode(token, properties.get_app_secret_key(), algorithm="HS256")
    except InvalidTokenError:
        return False

    user = user_service.get_user_by_user_name(decoded_token["sub"])

    if user is None:
        return False

    return True


def get_user_name(token):
    """
    Get the user name from the token.
    """

    if token is None:
        return None

    token = token.split(" ")[1]

    if token == TEST_BEARER_TOKEN:
        return "Test"

    try:
        decoded_token = jwt.decode(token, properties.get_app_secret_key(), algorithm="HS256")
    except InvalidTokenError:
        return None

    return decoded_token["sub"]


def get_user_id(token):
    """
    Get the ID of the user from the token.
    """

    user_name = get_user_name(token)

    if user_name is None:
        return None

    if user_name == "Test":
        user_name = "superuser"

    user = user_service.get_user_by_user_name(user_name)

    if user is None:
        return None

    return user["id"]


def are_roles_sufficient(token, required_roles):
    """
    Check if the user for whom the token has been issued has required roles.

    The user has to have only one of the required roles -- each role grants the access to the resource separately.
    """

    if token is None:
        return False

    token = token.split(" ")[1]

    if token == TEST_BEARER_TOKEN:
        if _is_test_bearer_enabled():
            return True
        else:
            return False

    if required_roles is None or len(required_roles) == 0:
        return True

    if _is_token_blacklisted(token):
        return False

    try:
        decoded_token = jwt.decode(token, properties.get_app_secret_key(), algorithm="HS256")
    except InvalidTokenError:
        return False

    user = user_service.get_user_by_user_name(decoded_token["sub"])

    if user is None:
        return False

    user_roles = user_roles_service.get_user_roles(user["user_name"])

    for user_role in user_roles:
        if user_role in required_roles:
            return True

    return False


def _is_test_bearer_enabled():
    test_bearer_enabled = properties.get_test_bearer_enabled()

    if test_bearer_enabled is None:
        raise BusinessError(f"Property {PROPERTY_TEST_BEARER_ENABLED} missing!")

    return bool(test_bearer_enabled)


def _is_token_blacklisted(token):
    blacklisted_token = blacklisted_token_repository.read_by_token(token)

    return blacklisted_token is not None


def blacklist_token(token):
    """
    Persist the given token as blacklisted.
    """

    token = token.split(" ")[1]

    blacklisted_token = BlacklistedTokenEntity()
    blacklisted_token.token = token

    blacklisted_token_repository.persist(blacklisted_token)
