"""
The module containing messages - all the texts in Polish returned by the application.
"""

PERSISTENCE_ERROR: str = "Błąd bazy danych."
APPLICATION_ERROR: str = "Błąd aplikacji."

INPUT_DATA_MISSING: str = "Brakujące dane: {}."
INPUT_DATA_INVALID: str = "Niepoprawne dane: {}."

LOGIN_ERROR: str = "Niepoprawny login lub hasło."

TOKEN_EXPIRED: str = "Autentykacja wygasła."
AUTHENTICATION_FAILED: str = "Niepowodzenie autentykacji."
ACCESS_DENIED: str = "Nie masz wystarczających uprawnień dla tej akcji."

ARG_NAMES: dict = {
    "user_name": "nazwa użytkownika",
    "password": "Hasło"
}

DBMSG_SUPERUSER_CREATED: str = "Superużytkownik został utworzony."
