"""
The module contains exception classes for the application.
"""

from artushima import error_messages

_ERROR_MESSAGE_TEMPLATE = "{} ({}.{})"


class ArtushimaError(Exception):
    """
    The base class for all application specific errors.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error occured
    """

    def __init__(self, message, class_name, method_name):

        super().__init__(_ERROR_MESSAGE_TEMPLATE.format(message, class_name, method_name))
        self.message = self.args[0]


class PersistenceError(ArtushimaError):
    """
    The error raised by repositories when a persistence action fails.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error ocured
    """

    pass


class BusinessError(ArtushimaError):
    """
    The error raised by services.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error ocured
    """

    pass


class TokenExpirationError(BusinessError):
    """
    The error raised when the authentication token has expired.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error ocured
    """

    pass


class TokenInvalidError(BusinessError):
    """
    The error raised when the authentication token is invalid.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error ocured
    """

    pass


class MissingInputDataError(BusinessError):
    """
    The error raised when an argument passed to a method is None or an empty string.

    Arguments:
        - arg_name - the name of the None-argument
        - class_name - the name of the class where the error occured
        - method_name - the name of the methord where the error occured
    """

    def __init__(self, arg_name, class_name, method_name):

        super().__init__(error_messages.ON_NONE_ARGUMENT.format(arg_name), class_name, method_name)
