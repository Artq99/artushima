"""
The module contains the application object and methods for its initialisation.
"""

import flask

_app = None

def init_app():
    """
    Initialise the application object.
    """

    global _app

    _app = flask.Flask(__name__)

    @_app.route("/")
    def index():
        return flask.render_template("index.html")

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
