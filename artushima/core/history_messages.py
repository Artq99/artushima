"""
Module containing definitions of the history messages for the entities and the method to reach to them.
"""

_history_messages = {
    "campaign: timeline entry created": "Utworzono podsumowanie sesji \"{}\"."
}


def get_message(key: str) -> str:
    """
    Get the history message under the given key.
    """

    message = _history_messages.get(key)

    if message is None:
        raise KeyError("History message not found!")

    return message
