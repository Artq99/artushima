"""
The module containing the definitions of error codes and the corresponding messages.
"""

_error_codes = {
    "default": "Wystąpił problem z aplikacją. Szczegóły błędu nie są znane. Skontaktuj się z administratorem.",
    # Technical errors
    "T0000": "Błąd aplikacji.",
    # Authentication related errors
    "AC002": "Ta operacja dostępna jest jedynie dla mistrza gry danej kampanii.",
    # Data related errors
    "D0000": "Brakujące dane.",
    "D0001": "Niepoprawny format daty. Akceptowany format to 'rrrr-mm-dd'.",
    # - user
    "DU001": "Brakujące dane: ID użytkownika",
    # - campaign
    "DC001": "Brakujące dane: ID kampanii",
    "DC002": "Kampania nie istnieje.",
    "DC003": "Brakujące dane: tytuł wpisu",
    "DC004": "Brakujące dane: data sesji"
}


def get_error_message(code):
    """
    Get an error message for a given error code.

    If no error message has been registered under the given code, the default message is given.
    """

    if code not in _error_codes.keys():
        return _error_codes["default"]

    return _error_codes[code]
