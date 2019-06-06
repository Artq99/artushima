"""
The module contains the application object and methods for its initialisation.
"""

import flask

from artushima.commons import logger
from artushima.commons import properties
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

    # registering views
    _app.register_blueprint(index_view.index_blueprint)

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

    get_app().run("localhost")
