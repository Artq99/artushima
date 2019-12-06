"""
The repository for the user entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.core import db_access
from artushima.core.exceptions import PersistenceError
from artushima.user.persistence.model import UserEntity


def persist(user):
    """
    Persist the given user in the database.

    Arguments:
        - user - an instance of UserEntity

    Returns:
        the persisted (updated) user
    """

    if not isinstance(user, UserEntity):
        raise ValueError("The argument is not UserEntity.")

    try:
        session = db_access.Session()
        session.add(user)
        session.flush()
    except SQLAlchemyError as err:
        raise PersistenceError("Error on persisting user: {}".format(str(err))) from err

    return user
