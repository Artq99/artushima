"""
Module containing methods parsing data.
"""

from datetime import date

from artushima.core.exceptions import DomainError


def parse_iso_date(date_string):
    """
    Parse a date string in ISO format to date.
    """

    try:
        return date.fromisoformat(date_string)
    except ValueError:
        raise DomainError("Incorrect date format!", "D0001")
