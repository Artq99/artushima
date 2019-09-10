"""
The module defining the edpoint for the authentication web-methods.
"""

import flask

from artushima.services import auth_service

auth_blueprint = flask.Blueprint("auth_endpoint", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/login", methods=["GET"])
def log_in() -> flask.Response:
    """
    Get the authentication token.

    Requires the request body:
        {
            "user_name": "<user_name>",
            "password": "<password>"
        }
    """

    user_name = None
    password = None

    if flask.request.json is not None:
        user_name = flask.request.json.get("user_name")
        password = flask.request.json.get("password")

    token_response = auth_service.log_in(user_name, password)

    return flask.jsonify(token_response), 200
