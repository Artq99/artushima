"""
The module containing utilities for tests.
"""

from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError


def create_persistence_error() -> PersistenceError:
    """
    Create an instance of the PersistenceError class for tests.

    Returns:
        an instance of the PersitenceError class
    """

    return PersistenceError("Persistence error.", "TestClass", "test_method")


def create_business_error() -> BusinessError:
    """
    Create an instance of the BusinessError class for tests.

    Returns:
        an instance of the BusinessError class
    """

    return BusinessError("Business error.", "TestClass", "test_method")
