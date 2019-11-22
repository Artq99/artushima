"""
The factory module for the application object.
"""

import flask


class App:
    """
    A wrapper class for the flask application object.

    It sets up all settings on initialization and is ready to run via the 'create_and_run' method.
    """

    def __init__(self):

        self.flask_app = flask.Flask(__name__)

        self.host = "localhost"
        self.port = 5000

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
