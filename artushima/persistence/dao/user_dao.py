"""
The data access object for the user entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.commons import logger
from artushima.commons.exceptions import PersistenceError
from artushima.persistence import pu
from artushima.persistence import model


def read_by_user_name(user_name: str):
    """
    Read a single user by its name.

    Arguments:
        - user_name - the name of the user to read

    Returns:
        a dict containing the data of the found user, None if it has not been found
    """

    try:
        user = pu.current_session.query(model.UserEntity) \
            .filter_by(user_name=user_name) \
            .first()
    except SQLAlchemyError as e:
        logger.log_error(str(e))
        raise PersistenceError("Error on reading data from the database.", __name__, read_by_user_name.__name__)

    if user is None:
        return None

    return user.map_to_dict()
