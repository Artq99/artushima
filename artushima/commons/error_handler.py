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


def handle(error: ArtushimaError) -> str:
    """
    process the given error and get a corresponding error message.

    Arguments:
        - error - the error to handle

    Returns:
        an error message related to the given error
    """

    if isinstance(error, PersistenceError):
        logger.log_error(str(error))
        return messages.PERSISTENCE_ERROR

    elif isinstance(error, TokenExpirationError):
        return messages.TOKEN_EXPIRED

    elif isinstance(error, TokenInvalidError):
        return messages.AUTHENTICATION_FAILED

    elif isinstance(error, BusinessError):
        logger.log_error(str(error))
        return messages.APPLICATION_ERROR

    return None
