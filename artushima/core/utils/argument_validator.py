"""
The module with utils for argument validation.
"""

from artushima.core.exceptions import BusinessError


def validate_str_arg(arg, arg_name):
    if arg is None:
        raise BusinessError(f"{arg_name} must be provided!")

    if not isinstance(arg, str):
        raise ValueError(f"{arg_name} must be a string value!")

    if not arg:
        raise BusinessError(f"{arg_name} must be provided!")
