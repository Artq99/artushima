"""
The factory module for the application object.
"""

import flask

from artushima.commons import logger
from artushima.core import properties


class App:
    """
    A wrapper class for the flask application object.

    It sets up all settings on initialization and is ready to run via the 'create_and_run' method.
    """

    def __init__(self):

        self.flask_app = flask.Flask(__name__)

        properties.init()

        self.host = properties.get_app_host()
        self.port = properties.get_app_port()

        logger.log_info("Application initialized.")

    def run(self):
        self.flask_app.run(self.host, self.port)


def create():
    """
    Create and return the application object.
    """

    return App()


def create_and_run():
    """
    Create the application object and run it immediately.
    """

    app = App()
    app.run()
