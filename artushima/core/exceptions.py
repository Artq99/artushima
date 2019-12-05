"""
The module contains exception classes for the application.
"""


class ArtushimaError(Exception):
    """
    The base class for all application specific errors.

    Arguments:
        - message - the error message
    """

    def __init__(self, message):

        super().__init__(message)
        self.message = message


class PersistenceError(ArtushimaError):
    """
    The error raised by repositories when a persistence action fails.

    Arguments:
        - message - the error message
    """


class BusinessError(ArtushimaError):
    """
    The error raised by services.

    Arguments:
        - message - the error message
    """
