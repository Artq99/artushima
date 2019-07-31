"""
The data access object for the user entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.commons import roles_utils
from artushima.commons.exceptions import PersistenceError
from artushima.persistence import pu
from artushima.persistence import model
from artushima.persistence.dao import dao_utils


def create(data: dict):
    """
    Create a new user.

    Arguments:
        - data - a dictionary containing the following entries:
            - user_name
            - password_hash
            - role

    Returns:
        a dictionary containing data of the newly persisted user
    """

    user = _map_to_new_entity(data)

    if user.user_name is None:
        raise PersistenceError("The argument 'user_name' cannot be None.", __name__, create.__name__)

    if user.role is None:
        raise PersistenceError("The argument 'role' cannot be None.", __name__, create.__name__)

    if not roles_utils.check_if_role_exists(user.role):
        raise PersistenceError("The role is invalid.", __name__, create.__name__)

    try:
        pu.current_session.add(user)
        pu.current_session.flush()
    except SQLAlchemyError as e:
        raise PersistenceError("Error on persisting data.", __name__, create.__name__) from e

    return user.map_to_dict()


def _map_to_new_entity(data: dict):
    """
    Map the given data to a newly created entity.
    """

    user = dao_utils.init_entity(model.UserEntity)
    user.user_name = _get_value_from_create_data(data, "user_name")
    user.password_hash = _get_value_from_create_data(data, "password_hash")
    user.role = _get_value_from_create_data(data, "role")

    return user


def _get_value_from_create_data(data: dict, key: str):
    """
    Get the value from the given data dict under the given key.

    Raises a PersistenceError when the key is missing.
    """

    if key not in data.keys():
        raise PersistenceError("The key '{}' is missing.".format(key), __name__, create.__name__)

    return data[key]


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
        raise PersistenceError("Error on reading data from the database.", __name__, read_by_user_name.__name__) from e

    if user is None:
        return None

    return user.map_to_dict()
