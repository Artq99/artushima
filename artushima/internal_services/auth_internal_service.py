"""
The module providing internal logic for the user authentication.
"""

import datetime

import jwt

from artushima.commons.exceptions import BusinessError
from artushima.commons import properties
from artushima.persistence.dao import blacklisted_token_dao


def generate_token(user_data: dict) -> bytes:
    """
    Generate a new authentication token for the given user.

    Arguments:
        - user_data - the data of the user for whom the token should be generated

    Returns:
        a new authentication token
    """

    if user_data is None:
        raise BusinessError("The argument 'user_data' cannot be None.", __name__, generate_token.__name__)

    token_expiration_time = properties.get_token_expiration_time()

    if token_expiration_time is None:
        raise BusinessError("The property 'token_expiration_time' is not present.", __name__, generate_token.__name__)

    payload = {
        "sub": user_data["user_name"],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(token_expiration_time))
    }

    return jwt.encode(payload, properties.get_app_secret_key(), algorithm="HS256")


def blacklist_token(token: str) -> dict:
    """
    Blacklist a token, so it cannot be used for the authentication anymore.

    Arguments:
        - token - the token to be blacklisted

    Returns:
        a dictionary containing the blacklisted token data
    """

    return blacklisted_token_dao.create(token)
