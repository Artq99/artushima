"""
The module contains the application object and methods for its initialisation.
"""

import flask

from artushima.commons import logger
from artushima.commons import properties
from artushima.persistence import pu
from artushima.persistence import model
from artushima.views import index_view

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

    # setting the secret key
    secret_key = properties.get_app_secret_key()

    if secret_key is None:
        logger.log_error("Application startup failed.")
        raise RuntimeError("Application startup failed.")

    _app.secret_key = secret_key

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
        logger.log_error("Application startup failed.")
        raise RuntimeError("Application startup failed.")

    app.run(host, port=port)
