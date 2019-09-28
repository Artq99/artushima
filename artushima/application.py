"""
The module contains the application object and methods for its initialisation.
"""

import flask

from artushima import constants
from artushima.commons import logger
from artushima.commons import properties
from artushima.persistence import pu
from artushima.persistence import model
from artushima.services import startup_service
from artushima.views import index_view
from artushima.web_api import auth_endpoint

_app = None


def init_app():
    """
    Initialise the application object.
    """

    global _app

    _app = flask.Flask(__name__)

    # initialising properties
    properties.init()

    # initialising the database
    pu.init_engine()
    model.Base.metadata.create_all(pu.SqlEngine)

    # registering views
    _app.register_blueprint(index_view.index_blueprint)

    # registering web-service endpoints
    _app.register_blueprint(auth_endpoint.auth_blueprint)

    # setting the secret key
    secret_key = properties.get_app_secret_key()

    if secret_key is None:
        _fail_startup()

    _app.secret_key = secret_key

    # creating superuser
    superuser_exists_response = startup_service.check_if_superuser_exists()

    if superuser_exists_response["status"] != constants.RESPONSE_STATUS_SUCCESS:
        _fail_startup()

    superuser_exists = superuser_exists_response["superuser_exists"]

    if not superuser_exists:
        superuser_response = startup_service.create_superuser()

        if superuser_response["status"] != constants.RESPONSE_STATUS_SUCCESS:
            _fail_startup()

    logger.log_info("The application has been initialised.")


def get_app():
    """
    Get the application object.

    If it has not been initialised, the method does it and then returns it.

    Returns: the application object.
    """

    global _app

    if _app is None:
        init_app()

    return _app


def start_app():
    """
    Start the application.
    """

    app = get_app()

    host = properties.get_app_host()
    port = properties.get_app_port()

    if host is None or port is None:
        _fail_startup()

    app.run(host, port=port)


def _fail_startup():
    message = "Application startup failed"
    logger.log_error(message)
    raise RuntimeError(message)
