"""
The module containing utilities for tests.
"""

from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
from artushima.commons.exceptions import MissingInputDataError


_TEST_CLASS = "TestClass"
_TEST_METHOD = "test_method"


def create_persistence_error() -> PersistenceError:
    """
    Create an instance of the PersistenceError class for tests.

    Returns:
        an instance of the PersitenceError class
    """

    return PersistenceError("Persistence error.", _TEST_CLASS, _TEST_METHOD)


def create_business_error() -> BusinessError:
    """
    Create an instance of the BusinessError class for tests.

    Returns:
        an instance of the BusinessError class
    """

    return BusinessError("Business error.", _TEST_CLASS, _TEST_METHOD)


def create_token_expiration_error() -> BusinessError:
    """
    Create an instance of the TokenExpirationError class for tests.

    Returns:
        an instance of the TokenExpirationError class
    """

    return TokenExpirationError("Token expiration error.", _TEST_CLASS, _TEST_METHOD)


def create_token_invalid_error() -> BusinessError:
    """
    Create an instance of the TokenInvalidError class for tests.

    Returns:
        an instance of the TokenInvalidError class
    """

    return TokenInvalidError("Token invalid error.", _TEST_CLASS, _TEST_METHOD)


def create_missing_input_data_error(arg_name: str) -> MissingInputDataError:
    """
    Create an instance of the MissingInputDataError class for tests.

    Arguments:
        - arg_name - the name of the missing argument

    Returns:
        an instance of the MissingInputDataError class
    """

    return MissingInputDataError(arg_name, _TEST_CLASS, _TEST_METHOD)
