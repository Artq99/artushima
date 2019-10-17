"""
The data access object for user history entity.
"""

from sqlalchemy.exc import SQLAlchemyError

from artushima.commons.exceptions import PersistenceError
from artushima.persistence import model
from artushima.persistence import pu
from artushima.persistence.dao import dao_utils


def create(data: dict) -> dict:
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


def _map_to_new_entity(data: dict) -> model.UserHistoryEntity:
    """
    Map the given data to a newly created entity.
    """

    user_history = dao_utils.init_entity(model.UserHistoryEntity)
    user_history.editor_name = data["editor_name"]
    user_history.message = data["message"]
    user_history.user_id = data["user_id"]

    return user_history
