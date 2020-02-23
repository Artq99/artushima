"""
The module defining the endpoint for managing and displaying users.
"""

import flask

from artushima.auth.auth_decorators import allow_authorized_with_roles
from artushima.commons import logger
from artushima.core import db_access
from artushima.user import user_service
from artushima.user.roles import ROLE_SHOW_USERS

USERS_BLUEPRINT = flask.Blueprint("users_endpoint", __name__, url_prefix="/api/users")


@USERS_BLUEPRINT.route("/list", methods=["GET"])
@allow_authorized_with_roles([ROLE_SHOW_USERS])
def user_list():
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
