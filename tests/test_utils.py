"""
The module containing utilities for tests.
"""

from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons.exceptions import TokenExpirationError
from artushima.commons.exceptions import TokenInvalidError
from artushima.commons.exceptions import MissingInputDataError
from artushima.commons.exceptions import InvalidInputDataError
from artushima.commons.exceptions import MissingApplicationPropertyError
from artushima.commons.exceptions import InvalidApplicationPropertyValueError


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


def create_invalid_input_data_error(arg_name: str) -> InvalidInputDataError:
    """
    Create an instance of the InvalidInputDataError class for tests.

    Arguments:
        - arg_name - the name of the invalid argument

    Returns:
        an instance of the InvalidInputDataError class
    """

    return InvalidInputDataError(arg_name, _TEST_CLASS, _TEST_METHOD)


def create_missing_application_property_error(property_name: str) -> MissingApplicationPropertyError:
    """
    Create an instance of the MissingApplicationPropertyError class for tests.

    Arguments:
        - property_name - the name of the missing property

    Returns:
        an instance of the MissingApplicationPropertyError class
    """

    return MissingApplicationPropertyError(property_name, _TEST_CLASS, _TEST_METHOD)


def create_invalid_application_property_value_error(property_name: str) -> InvalidApplicationPropertyValueError:
    """
    Create an instance of the InvalidApplicationPropertyValueError class for tests.

    Arguments:
        - property_name - the name of the invalid property

    Returns:
        an instance of the InvalidApplicationPropertyValueError class
    """

    return InvalidApplicationPropertyValueError(property_name, _TEST_CLASS, _TEST_METHOD)
