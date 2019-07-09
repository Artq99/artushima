"""
The module containing utilities for services.
"""

from artushima import constants


def create_response(status, message=None, **kwargs):
    """
    Create a response dictionary, common for all services.

    Arguments:
        - status - the status of the operation: 'success' or 'failure'

    Key word arguments:
        - message - the message of the response; default: None
        - * - any other key word argument will be converted to a key-value pair in the response dictionary

    Returns:
        a response dictionary
    """

    response = {
        "status": status,
        "message": message
    }

    for key in kwargs.keys():
        response[key] = kwargs[key]

    return response


def create_response_success(message=None, **kwargs):
    """
    Create a response dictionary, common for all services, with the status 'success'.

    Key word arguments:
        - message - the message of the response; default: None
        - * - any other key word argument will be converted to a key-value pair in the response dictionary

    Returns:
        a response dictionary
    """

    return create_response(constants.RESPONSE_STATUS_SUCCESS, message=message, **kwargs)


def create_failure(message=None, **kwargs):
    """
    Create a response dictionary, common for all services, with the status 'failure'.

    Key word arguments:
        - message - the message of the response; default: None
        - * - any other key word argument will be converted to a key-value pair in the response dictionary

    Returns:
        a response dictionary
    """

    return create_response(constants.RESPONSE_STATUS_FAILURE, message=message, **kwargs)
