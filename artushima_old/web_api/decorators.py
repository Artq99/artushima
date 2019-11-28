"""
The module containing decorators for the web-service endpoints.
"""

import flask

import functools

from artushima import constants
from artushima import messages
from artushima.services import auth_service


def auth_required(roles=[]):
    """
    The decorator that limits the usage of an endpoint to users that are logged in and have required roles.
    """

    def auth_required_internal(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if (flask.request.headers is None) or ("Authorization" not in flask.request.headers):
                return flask.abort(401)

            token = flask.request.headers.get("Authorization").split(" ")[1]

            response = auth_service.authenticate(token, roles)

            if response["status"] == constants.RESPONSE_STATUS_FAILURE:
                return flask.abort(_evaluate_http_error(response))

            return func(*args, **kwargs)

        return wrapper

    return auth_required_internal


def _evaluate_http_error(response: dict) -> int:
    if response["message"] == messages.ACCESS_DENIED:
        return 403
    else:
        return 401
