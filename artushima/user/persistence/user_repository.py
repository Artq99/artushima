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


def read_by_id(id):
    """
    Read the user of the given ID.
    """

    try:
        session: Session = db_access.Session()
        return session.query(UserEntity).filter_by(id=id).first()
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading user by the ID {id}: {str(err)}") from err


def read_by_user_name(name):
    """
    Read the user of the given name.
    """

    try:
        session: Session = db_access.Session()
        return session.query(UserEntity).filter_by(user_name=name).first()
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading user by the user name {name}: {str(err)}") from err


def read_all():
    """
    Read all users.
    """

    session: Session = db_access.Session()

    try:
        users = session.query(UserEntity).all()
        return users
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading all users: {str(err)}") from err
