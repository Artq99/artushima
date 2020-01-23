"""
The module contains exception classes for the application.
"""


class ArtushimaError(Exception):
    """
    The base class for all application specific errors.
    """

    def __init__(self, message):

        super().__init__(message)
        self.message = message


class PersistenceError(ArtushimaError):
    """
    The error raised by repositories when a persistence action fails.
    """


class BusinessError(ArtushimaError):
    """
    The error raised by services.
    """
