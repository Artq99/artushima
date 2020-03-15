"""
The module contains the endpoint for the index page.
"""

import flask
from flask import Blueprint

INDEX_BLUEPRINT = Blueprint("index_view", __name__, url_prefix="/")


@INDEX_BLUEPRINT.route("/")
@INDEX_BLUEPRINT.route("/dashboard")
@INDEX_BLUEPRINT.route("/login")
@INDEX_BLUEPRINT.route("/users/list")
@INDEX_BLUEPRINT.route("/users/add")
@INDEX_BLUEPRINT.route("/my_campaigns/list")
def index():
    """
    The endpoint for '/'.
    """

    return flask.render_template("index.html")
