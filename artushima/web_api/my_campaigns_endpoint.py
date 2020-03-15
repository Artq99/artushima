"""
The module defining the endpoint for viewing and managing campaigns by the
game master.
"""

import flask

from artushima.auth import auth_service
from artushima.auth.auth_decorators import allow_authorized_with_roles
from artushima.campaign import campaign_service
from artushima.commons import logger
from artushima.core import db_access
from artushima.core.exceptions import BusinessError
from artushima.user.roles import ROLE_SHOW_OWNED_CAMPAIGNS

MY_CAMPAIGNS_BLUEPRINT = flask.Blueprint("my_campaigns_endpoint", __name__, url_prefix="/api/my_campaigns")


@MY_CAMPAIGNS_BLUEPRINT.route("/list", methods=["GET"])
@allow_authorized_with_roles([ROLE_SHOW_OWNED_CAMPAIGNS])
def my_campaigns_list():
    """
    Get the list of campaigns belonging to the currently logged in user.
    """

    user_id = None

    if flask.request.headers.get("Authorization") is not None:
        token = flask.request.headers.get("Authorization")
        user_id = auth_service.get_user_id(token)

    db_session = db_access.Session()

    try:
        campaigns = campaign_service.get_campaigns_by_gm_id(user_id)

        result = list()

        for campaign in campaigns:
            result.append({
                "id": campaign["id"],
                "campaignName": campaign["campaign_name"]
            })

        return flask.jsonify({
            "status": "success",
            "message": "",
            "myCampaigns": result
        }), 200

    except BusinessError as err:
        db_session.rollback()

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
