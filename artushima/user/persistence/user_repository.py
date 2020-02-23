"""
The repository for the user entity.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from artushima.core import db_access
from artushima.core.exceptions import PersistenceError
from artushima.user.persistence.model import UserEntity


def persist(user):
    """
    Persist the given user in the database.
    """

    if not isinstance(user, UserEntity):
        raise ValueError("The argument is not UserEntity.")

    try:
        session: Session = db_access.Session()
        session.add(user)
        session.flush()
        return user
    except SQLAlchemyError as err:
        raise PersistenceError("Error on persisting user: {}".format(str(err))) from err


def read_by_user_name(name):
    """
    Read the user of the given name.
    """

    try:
        session: Session = db_access.Session()
        user = session.query(UserEntity).filter_by(user_name=name).first()
        return user
    except SQLAlchemyError as err:
        raise PersistenceError("Error on reading user: {}".format(str(err))) from err


def read_all():
    """
    Read all users.
    """

    try:
        session: Session = db_access.Session()
        users = session.query(UserEntity).all()
        return users
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading all users: {str(err)}") from err
