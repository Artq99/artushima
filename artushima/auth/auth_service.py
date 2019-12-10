"""
The module dealing with user authenication.
"""

from datetime import datetime, timedelta

import jwt
import werkzeug

from artushima.core import properties
from artushima.core.exceptions import BusinessError
from artushima.core.properties import PROPERTY_TOKEN_EXPIRATION_TIME
from artushima.user import user_roles_service, user_service


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
