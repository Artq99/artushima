"""
The module contains the endpoint for the index page.
"""

import flask

index_blueprint = flask.Blueprint("index_view", __name__, url_prefix="/")


@index_blueprint.route("/")
@index_blueprint.route("/dashboard")
@index_blueprint.route("/login")
def index():
    """
    The endpoint for '/'.
    """

    return flask.render_template("index.html")
