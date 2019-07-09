"""
The internal service dealing with the history of the user entity.
"""

from artushima.persistence.dao import user_history_dao


def create_user_history_entry(data: dict):
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

    return user_history_dao.create(data)
