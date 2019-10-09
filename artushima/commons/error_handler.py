"""
The util module dealing with error handling.
"""

from artushima import messages
from artushima.commons import logger
from artushima.commons.exceptions import ArtushimaError
from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
from artushima.commons.exceptions import MissingInputDataError


def handle(error: ArtushimaError) -> str:
    """
    process the given error and get a corresponding error message.

    Arguments:
        - error - the error to handle

    Returns:
        an error message related to the given error
    """

    logger.log_error(str(error))

    if isinstance(error, PersistenceError):
        return messages.PERSISTENCE_ERROR

    elif isinstance(error, TokenExpirationError):
        return messages.TOKEN_EXPIRED

    elif isinstance(error, TokenInvalidError):
        return messages.AUTHENTICATION_FAILED

    elif isinstance(error, MissingInputDataError):
        arg_name = error.arg_name

        if arg_name in messages.ARG_NAMES.keys():
            arg_name = messages.ARG_NAMES[arg_name]

        return messages.INPUT_DATA_MISSING.format(arg_name)

    elif isinstance(error, BusinessError):
        return messages.APPLICATION_ERROR

    return None
