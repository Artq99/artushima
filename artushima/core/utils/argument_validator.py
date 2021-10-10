"""
The module with utils for argument validation.
"""

from artushima.core.exceptions import BusinessError, DomainError


def validate_int_arg(arg, arg_name):
    """
    Check if the argument is an integer.
    """

    if arg is None:
        raise BusinessError(f"Brakujące dane: {arg_name}")

    if not isinstance(arg, int):
        raise ValueError(f"{arg_name} must be an int value!")


def validate_str_arg(arg, arg_name):
    """
    Check if the argument is a non-empty string.
    """

    if arg is None:
        raise BusinessError(f"Brakujące dane: {arg_name}")

    if not isinstance(arg, str):
        raise ValueError(f"{arg_name} must be a string value!")

    if not arg:
        raise BusinessError(f"Brakujące dane: {arg_name}")


def validate_list_arg(arg, arg_name):
    """
    Check if the argument is a list.
    """

    if arg is None:
        raise BusinessError(f"Brakujące dane: {arg_name}")

    if not isinstance(arg, list):
        raise ValueError(f"{arg_name} must be a list!")


def validate_list_arg_nullable(arg, arg_name):
    """
    Check if the argument is a list or None.
    """

    if (arg is not None) and (not isinstance(arg, list)):
        raise ValueError(f"{arg_name} must be a list!")


def assert_str(arg, error_code, http_status=200):
    """
    Check if the argument is a string.
    """

    if arg is None:
        raise DomainError("Parameter not provided!", error_code, http_status)

    if not isinstance(arg, str):
        raise ValueError("Parameter not a string!")


def assert_str_or_none(arg):
    """
    Check if the argument is a string or none.
    """

    if (not isinstance(arg, str)) and (arg is not None):
        raise ValueError("Paramter not a string!")


def assert_int(arg, error_code, http_status=200):
    """
    Check if the argument is an integer.
    """

    if arg is None:
        raise DomainError("Parameter not provided!", error_code, http_status)

    if not isinstance(arg, int):
        raise ValueError("Parameter not an integer!")
