"""
The internal service dealing with the history of the user entity.
"""

from artushima.commons.exceptions import MissingInputDataError
from artushima.persistence.dao import user_history_dao


_ARG_DATA = "data"
_ARG_EDITOR_NAME = "editor_name"
_ARG_MESSAGE = "message"
_ARG_USER_ID = "user_id"


def create_user_history_entry(data: dict) -> dict:
    """
    Create an entry to the user entity.

    Arguments:
        - data - a dictionary containing the following entries:
            - editor_name - the name of the subject that caused the changes
            - message - the description of the changes
            - user_id - the ID of the user entity

    Returns:
        a dictionary containing data of the newly created entry
    """

    _validate_input_data_for_entry_creation(data)

    return user_history_dao.create(data)


def _validate_input_data_for_entry_creation(data: dict) -> None:

    if data is None:
        raise MissingInputDataError(_ARG_DATA, __name__, create_user_history_entry.__name__)

    if (_ARG_EDITOR_NAME not in data.keys()) or (not data[_ARG_EDITOR_NAME]):
        raise MissingInputDataError(_ARG_EDITOR_NAME, __name__, create_user_history_entry.__name__)

    if (_ARG_MESSAGE not in data.keys()) or (not data[_ARG_MESSAGE]):
        raise MissingInputDataError(_ARG_MESSAGE, __name__, create_user_history_entry.__name__)

    if (_ARG_USER_ID not in data.keys()) or (not data[_ARG_USER_ID]):
        raise MissingInputDataError(_ARG_USER_ID, __name__, create_user_history_entry.__name__)
