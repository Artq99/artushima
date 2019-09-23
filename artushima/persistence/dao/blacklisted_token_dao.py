"""
The data access object for the blacklisted token entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima import error_messages
from artushima.commons.exceptions import PersistenceError
from artushima.persistence import pu
from artushima.persistence import model


def create(token: str) -> dict:
    """
    Create a new blacklisted token.

    Arguments:
        - token - the token to be blacklisted

    Returns:
        a dictionary containing data of the newly persisted blacklisted token
    """

    if token is None:
        raise PersistenceError("The argument 'token' cannot be None.", __name__, create.__name__)

    blacklisted_token = model.BlacklistedTokenEntity()
    blacklisted_token.token = token

    try:
        pu.current_session.add(blacklisted_token)
        pu.current_session.flush()
    except SQLAlchemyError as e:
        raise PersistenceError("Error on persisting data.", __name__, create.__name__) from e

    return blacklisted_token.map_to_dict()


def read_by_token(token: str) -> dict:
    """
    Read the blacklisted token data from the database by the given token.

    Arguments:
        - token - the token to read

    Returns:
        a dictionary containing blacklisted token data if the token was found,
        None otherwise
    """

    try:
        token = pu.current_session.query(model.BlacklistedTokenEntity) \
            .filter_by(token=token) \
            .first()
    except SQLAlchemyError as e:
        raise PersistenceError(error_messages.ON_READING_DATA, __name__, read_by_token.__name__) from e

    if token is None:
        return None

    return token.map_to_dict()
