"""
The module defining the edpoint for the authentication web-methods.
"""

import flask

from artushima.services import auth_service
from artushima.web_api.decorators import auth_required

auth_blueprint = flask.Blueprint("auth_endpoint", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/login", methods=["POST"])
def log_in() -> flask.Response:
    """
    Get the authentication token.

    Requires the request body:
        {
            "userName": "<userName>",
            "password": "<password>"
        }
    """

    user_name = None
    password = None

    if flask.request.json is not None:
        user_name = flask.request.json.get("userName")
        password = flask.request.json.get("password")

    token_response = auth_service.log_in(user_name, password)

    return flask.jsonify(token_response), 200


@auth_blueprint.route("/logout", methods=["POST"])
@auth_required()
def log_out() -> flask.Response:
    """
    Blacklist the authentication token.
    """

    token = flask.request.headers.get("Authorization").split(" ")[1]
    token_response = auth_service.log_out(token)

    return flask.jsonify(token_response), 200
