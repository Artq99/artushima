"""
The data access object for user history entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.commons.exceptions import PersistenceError
from artushima.persistence import model
from artushima.persistence import pu
from artushima.persistence.dao import dao_utils


def create(data: dict):
    """
    Create a new entry for the history of an user entity.

    Arguments:
        - data - a dictionary containing the following entries:
            - editor_name - the name of the subject causing the changes
            - message - the description of the changes
            - user_id - the id of the user entity

    Returns:
        a dictionary containing the data of the newly persisted entry
    """

    user_history = _map_to_new_entity(data)

    try:
        pu.current_session.add(user_history)
        pu.current_session.flush()
    except SQLAlchemyError as e:
        raise PersistenceError("Error on persisting data.", __name__, create.__name__) from e

    return user_history.map_to_dict()


def _map_to_new_entity(data: dict):
    """
    Map the given data to a newly created entity.
    """

    user_history = dao_utils.init_entity(model.UserHistoryEntity)
    user_history.editor_name = _get_value_from_create_data(data, "editor_name")
    user_history.message = _get_value_from_create_data(data, "message")
    user_history.user_id = _get_value_from_create_data(data, "user_id")

    return user_history


def _get_value_from_create_data(data: dict, key: str):
    """
    Get the value from the given data dict under the given key.

    Raises a PersistenceError when the key is missing; The error location is set to the create method of this module.
    """

    if key not in data.keys():
        raise PersistenceError("The argument '{}' is missing.".format(key), __name__, create.__name__)

    return data[key]
