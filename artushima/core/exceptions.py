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


class DomainError(ArtushimaError):
    """
    Error raised when there was no technical failure, but something went wrong for a reason related to
    the domain's logic.
    """

    def __init__(self, message, error_code, http_status=200):

        super().__init__(message)
        self.error_code = error_code
        self.http_status = http_status
