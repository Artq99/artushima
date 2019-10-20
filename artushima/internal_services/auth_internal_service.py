"""
The module providing internal logic for the user authentication.
"""

import datetime

import jwt
from jwt import InvalidTokenError
from jwt import ExpiredSignatureError
import werkzeug

from artushima import error_messages
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
from artushima.commons.exceptions import MissingInputDataError
from artushima.commons.exceptions import MissingApplicationPropertyError
from artushima.commons.exceptions import InvalidApplicationPropertyValueError
from artushima.commons import properties
from artushima.persistence.dao import blacklisted_token_dao


_ARG_USER_NAME: str = "user_name"
_ARG_TOKEN: str = "token"
_ARG_PASSWORD: str = "password"
_ARG_PWHASH: str = "pwhash"
_PROPERTY_TOKEN_EXPIRATION_TIME: str = "token_expiration_time"
_HS256: str = "HS256"


def generate_token(user_name: str) -> bytes:
    """
    Generate a new authentication token for the given user.

    Arguments:
        - user_data - the data of the user for whom the token should be generated

    Returns:
        a new authentication token
    """

    _validate_user_name(user_name)
    token_expiration_time: int = _get_token_expiration_time()
    payload: dict = _create_token_payload(user_name, token_expiration_time)

    return jwt.encode(payload, properties.get_app_secret_key(), algorithm=_HS256)


def _validate_user_name(user_name: str) -> str:

    if not user_name:
        raise MissingInputDataError(_ARG_USER_NAME, __name__, generate_token.__name__)


def _get_token_expiration_time() -> int:

    token_expiration_time: str = properties.get_token_expiration_time()

    if token_expiration_time is None:
        raise MissingApplicationPropertyError(_PROPERTY_TOKEN_EXPIRATION_TIME, __name__, generate_token.__name__)

    try:
        return int(token_expiration_time)
    except ValueError:
        raise InvalidApplicationPropertyValueError(_PROPERTY_TOKEN_EXPIRATION_TIME, __name__, generate_token.__name__)


def _create_token_payload(user_name: str, token_expiration_time: int) -> dict:

    return {
        "sub": user_name,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=token_expiration_time)
    }


def blacklist_token(token: str) -> dict:
    """
    Blacklist a token, so it cannot be used for the authentication anymore.

    Arguments:
        - token - the token to be blacklisted

    Returns:
        a dictionary containing the blacklisted token data
    """

    if not token:
        raise MissingInputDataError(_ARG_TOKEN, __name__, blacklist_token.__name__)

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
        raise MissingInputDataError(_ARG_TOKEN, __name__, check_if_token_is_blacklisted.__name__)

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
        decoded_token = jwt.decode(token, properties.get_app_secret_key(), algorithm=_HS256)
    except ExpiredSignatureError as e:
        raise TokenExpirationError(error_messages.ON_EXPIRED_SIGNATURE, __name__, decode_token.__name__) from e
    except InvalidTokenError as e:
        raise TokenInvalidError(error_messages.ON_INVALID_TOKEN, __name__, decode_token.__name__) from e

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
        raise MissingInputDataError(_ARG_PASSWORD, __name__, check_password.__name__)

    if not pwhash:
        raise MissingInputDataError(_ARG_PWHASH, __name__, check_password.__name__)

    return werkzeug.check_password_hash(pwhash, password)
