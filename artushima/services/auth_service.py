"""
The service providing methods for user to log in, log out and authenticate.
"""

import flask
import werkzeug

from artushima.commons.exceptions import PersistenceError
from artushima.commons.exceptions import BusinessError
from artushima.commons import logger
from artushima.internal_services import user_internal_service
from artushima.internal_services import auth_internal_service
from artushima.services import service_utils


def log_in(user_name: str, password: str) -> dict:
    """
    Log in to the application and generate an authentication token for continuous authentication.

    Arguments:
        - user_name - the login
        - password - the password

    Returns:
        a service response with the status of the operation and the list of messages in case of failure.
    """

    if user_name is None:
        return service_utils.create_response_failure("Brakująca nazwa użytkownika.")

    if password is None:
        return service_utils.create_response_failure("Brakujące hasło.")

    try:
        user = user_internal_service.read_user_by_user_name(user_name)
    except PersistenceError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Błąd odczytu danych.")
    except BusinessError as e:
        logger.log_error(str(e))
        return service_utils.create_response_failure("Błąd aplikacji.")

    if user is None:
        return service_utils.create_response_failure("Niepoprawny login lub hasło.")

    if not werkzeug.check_password_hash(user["password_hash"], password):
        return service_utils.create_response_failure("Niepoprawny login lub hasło.")

    flask.session["user_name"] = user["user_name"]
    flask.session["token"] = auth_internal_service.generate_token(user)

    return service_utils.create_response_success()
