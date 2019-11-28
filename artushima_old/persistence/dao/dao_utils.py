"""
The module containing utilities for DAOs.
"""

from datetime import datetime


def init_entity(entity_class):
    """
    Initialise a new instance of an entity of the given class.

    The returned entity has the 'opt_lock' field set to 0 and 'created_on' and 'modified_on' set to the result of the
    datetime.datetime.now function.

    Arguments:
        - entity_class - the class of the entity to initialise

    Returns:
        new entity instance
    """

    entity = entity_class()
    entity.opt_lock = 0

    timestamp = datetime.now()

    entity.created_on = timestamp
    entity.modified_on = timestamp

    return entity
