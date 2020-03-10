"""
The module defining the endpoint for managing and displaying users.
"""

import flask

from artushima.auth import auth_service
from artushima.auth.auth_decorators import allow_authorized_with_roles
from artushima.commons import logger
from artushima.core import db_access
from artushima.core.exceptions import BusinessError
from artushima.user import user_service
from artushima.user.roles import ROLE_CREATE_USER, ROLE_SHOW_USERS

USERS_BLUEPRINT = flask.Blueprint("users_endpoint", __name__, url_prefix="/api/users")


@USERS_BLUEPRINT.route("/list", methods=["GET"])
@allow_authorized_with_roles([ROLE_SHOW_USERS])
def users_list():
    """
    Get the list of all users.
    """

    db_session = db_access.Session()

    try:
        users = user_service.get_all_users()

        result = list()

        for user in users:
            result.append({
                "id": user["id"],
                "userName": user["user_name"]
            })

        return flask.jsonify({
            "status": "success",
            "message": "",
            "users": result
        }), 200

    except Exception as err:
        logger.log_error(str(err))
        db_session.rollback()

        return flask.jsonify({
            "status": "failure",
            "message": "Błąd aplikacji"
        }), 500

    finally:
        db_session.close()


@USERS_BLUEPRINT.route("/add", methods=["POST"])
@allow_authorized_with_roles([ROLE_CREATE_USER])
def users_add():
    """
    Add a new user.

    Requires the following request body:
        {
            "userName": "<userName>",
            "password": "<password>",
            "roles": [ (optional)
                <role1>,
                ...
            ]
        }
    """

    editor_name = None
    user_name = None
    password = None
    roles = None

    if flask.request.headers.get("Authorization") is not None:
        token = flask.request.headers.get("Authorization")
        editor_name = auth_service.get_user_name(token)

    if flask.request.json is not None:
        user_name = flask.request.json.get("userName")
        password = flask.request.json.get("password")
        roles = flask.request.json.get("roles")

    db_session = db_access.Session()

    try:
        user_service.create_user(editor_name, user_name, password, roles)
        db_session.commit()

        return flask.jsonify({
            "status": "success",
            "message": ""
        }), 200

    except BusinessError as err:
        db_session.rollback

        return flask.jsonify({
            "status": "failure",
            "message": err.message
        }), 200

    except Exception as err:
        logger.log_error(str(err))
        db_session.rollback()

        return flask.jsonify({
            "status": "failure",
            "message": "Błąd aplikacji."
        }), 500

    finally:
        db_session.close()
