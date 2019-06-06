"""
The module contains exception classes for the application.
"""

_ERROR_MESSAGE_TEMPLATE = "%s (%s.%s)"


class Error(Exception):
    """
    The base class for all application specific errors.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name - the name of the method where the error occured
    """

    def __init__(self, message, class_name, method_name):
        super().__init__(_ERROR_MESSAGE_TEMPLATE % (message, class_name, method_name))
        self.message = self.args[0]


class PersistenceError(Error):
    """
    The error raised by repositories when a persistence action fails.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name = the name of the method where the error ocured
    """

    pass


class BusinessError(Error):
    """
    The error raised by services.

    Arguments:
        - message - the error message
        - class_name - the name of the class where the error occured
        - method_name = the name of the method where the error ocured
    """

    pass
