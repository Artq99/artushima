"""
The module providing internal logic for the user authentication.
"""

import datetime

import jwt
from jwt import InvalidTokenError
from jwt import ExpiredSignatureError
import werkzeug

from artushima import error_messages
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
from artushima.commons.exceptions import MissingInputDataError
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

    if not token:
        raise MissingInputDataError("token", __name__, blacklist_token.__name__)

    return blacklisted_token_dao.create(token)


def check_if_token_is_blacklisted(token: str) -> bool:
    """
    Check if the token has been blacklisted.

    Arguments:
        - token - the token to check

    Returns:
        True, if the token has been blacklisted, False otherwise
    """

    if not token:
        raise MissingInputDataError("token", __name__, check_if_token_is_blacklisted.__name__)

    blacklisted_token = blacklisted_token_dao.read_by_token(token)

    return blacklisted_token is not None


def decode_token(token: str) -> dict:
    """
    Decode the authentication token.

    Arguments:
        - token - the token to be decoded

    Returns:
        a dictionary containing the decoded token data
    """

    try:
        decoded_token = jwt.decode(token, properties.get_app_secret_key(), algorithm="HS256")
    except ExpiredSignatureError as e:
        raise TokenExpirationError("Authentication token signature has expired.",
                                   __name__, decode_token.__name__) from e
    except InvalidTokenError as e:
        raise TokenInvalidError("The token is invalid.", __name__, decode_token.__name__) from e

    return decoded_token


def check_password(password: str, pwhash: str) -> bool:
    """
    Check if the given password corresponds to the given hash.

    Arguments:
        - password - the user password
        - pwhash - the password hash

    Returns:
        True, if the password can be authenticated with the given hash, False otherwise
    """

    if not password:
        raise MissingInputDataError("password", __name__, check_password.__name__)

    if not pwhash:
        raise MissingInputDataError("pwhash", __name__, check_password.__name__)

    return werkzeug.check_password_hash(pwhash, password)
