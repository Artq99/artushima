"""
The module defining the endpoint for viewing and managing campaigns by the
game master.
"""

import flask
from datetime import date

from artushima.auth import auth_service
from artushima.auth.auth_decorators import allow_authorized_with_roles
from artushima.campaign import campaign_service
from artushima.commons import logger
from artushima.core import db_access
from artushima.core.exceptions import BusinessError
from artushima.user.roles import ROLE_SHOW_OWNED_CAMPAIGNS, ROLE_START_CAMPAIGN

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


@MY_CAMPAIGNS_BLUEPRINT.route("/start", methods=["POST"])
@allow_authorized_with_roles([ROLE_START_CAMPAIGN])
def my_campaigns_start():
    """
    Start a new campaign, with the logged in user as the game master.

    Requires the following request body:
    {
        "campaignName": "<the name of the new campaign>",
        "beginDate": "<The in-game starting date of the campaign in the ISO format: YYYY-MM-DD>"
    }
    """

    # The decorator has assured that the user had been logged in.
    # No need for checking the existence of the header at this point.
    token = flask.request.headers.get("Authorization")
    user_id = auth_service.get_user_id(token)
    user_name = auth_service.get_user_name(token)

    # If the request doesn't contain JSON, it is a bad request.
    if not flask.request.is_json:
        return flask.abort(400)

    # Getting data from the request body.
    campaign_name = flask.request.json.get("campaignName")
    begin_date = flask.request.json.get("beginDate")

    # Validating the arguments.
    if not campaign_name:
        return _create_failure("Brakująca nazwa kampanii."), 200
    if not begin_date:
        return _create_failure("Brakująca data początku kampanii."), 200

    # Parsing and validating the begin date.
    begin_date = _parse_date(begin_date)
    if begin_date is None:
        return _create_failure("Data początku kampanii jest niepoprawna."), 200

    # Opening a DB session.
    db_session = db_access.Session()

    # Creating and persisting the campaign.
    try:
        campaign_service.create_campaign(user_name, campaign_name, begin_date, 0, user_id, user_name)
        db_session.commit()
        return _create_success(), 200
    except Exception as err:
        logger.log_error(str(err))
        db_session.rollback()
        return _create_failure("Błąd aplikacji."), 500
    finally:
        db_session.close()


def _create_success():
    return flask.jsonify({
        "status": "success",
        "message": ""
    })


def _create_failure(message):
    return flask.jsonify({
        "status": "failure",
        "message": message
    })


def _parse_date(date_str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None
