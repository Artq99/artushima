"""
The module defining the edpoint for the authentication web-methods.
"""

import flask

from artushima.auth import auth_service
from artushima.commons import logger
from artushima.core import db_access
from artushima.core.exceptions import BusinessError

AUTH_BLUEPRINT = flask.Blueprint("auth_endpoint", __name__, url_prefix="/api/auth")


@AUTH_BLUEPRINT.route("/login", methods=["POST"])
def log_in():
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

    if not user_name:
        return flask.jsonify({
            "status": "failure",
            "message": "Brakująca nazwa użytkownika."
        }), 200

    if not password:
        return flask.jsonify({
            "status": "failure",
            "message": "Brakujące hasło."
        }), 200

    db_session = db_access.Session()

    try:
        current_user = auth_service.log_in(user_name, password)
        db_session.commit()

    except BusinessError:
        return flask.jsonify({
            "status": "failure",
            "message": "Błąd autentykacji"
        }), 401

    except Exception as err:
        logger.log_error(str(err))
        db_session.rollback()

        return flask.jsonify({
            "status": "failure",
            "message": "Błąd aplikacji"
        }), 500

    finally:
        db_session.close()

    return flask.jsonify({
        "status": "success",
        "message": "",
        "currentUser": {
            "userName": current_user["user_name"],
            "token": current_user["token"],
            "roles": current_user["roles"]
        }
    }), 200


@AUTH_BLUEPRINT.route("/logout", methods=["POST"])
def log_out():
    """
    Blacklist the token.

    Requires the user to be logged in.
    """

    token = flask.request.headers.get("Authorization")

    db_session = db_access.Session()

    try:
        if not auth_service.is_token_ok(token):

            return flask.jsonify({
                "status": "failure",
                "message": "Błąd autoryzacji"
            }), 401

        auth_service.blacklist_token(token)
        db_session.commit()

    except Exception as err:
        logger.log_error(str(err))
        db_session.rollback()

        return flask.jsonify({
            "status": "failure",
            "message": "Błąd aplikacji"
        }), 500

    finally:
        db_session.close()

    return flask.jsonify({
        "status": "success",
        "message": ""
    }), 200
