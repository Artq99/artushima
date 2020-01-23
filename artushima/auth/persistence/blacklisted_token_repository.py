"""
The repository for the blacklisted token entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.auth.persistence.model import BlacklistedTokenEntity
from artushima.core import db_access
from artushima.core.exceptions import PersistenceError


def persist(blacklisted_token):
    """
    Persist the given blacklisted token in the database.
    """

    if not isinstance(blacklisted_token, BlacklistedTokenEntity):
        raise ValueError("The argument is not BlacklistedTokenEntity.")

    try:
        session = db_access.Session()
        session.add(blacklisted_token)
        session.flush()
        return blacklisted_token
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on persisting blacklisted token: {str(err)}")


def read_by_token(token):
    """
    Read a blacklisted token entry by the token value.
    """

    try:
        session = db_access.Session()
        blacklisted_token = session.query(BlacklistedTokenEntity).filter_by(token=token).first()
        return blacklisted_token
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading blacklisted token: {token}") from err
