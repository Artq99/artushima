"""
The module defining the endpoint for viewing and managing campaigns by the
game master.
"""

from datetime import date

import flask
from artushima.auth import auth_service
from artushima.auth.auth_decorators import allow_authorized_with_roles
from artushima.campaign import campaign_mapper, campaign_service
from artushima.commons import logger
from artushima.core import db_access
from artushima.core.error_codes import get_error_message
from artushima.core.exceptions import BusinessError, DomainError
from artushima.user.roles import (ROLE_CREATE_SESSION_SUMMARY,
                                  ROLE_SHOW_OWNED_CAMPAIGNS,
                                  ROLE_START_CAMPAIGN,
                                  ROLE_VIEW_CAMPAIGN_TIMELINE)

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


@MY_CAMPAIGNS_BLUEPRINT.route("/details/<int:campaign_id>", methods=["GET"])
@allow_authorized_with_roles([ROLE_SHOW_OWNED_CAMPAIGNS])
def my_campaigns_details(campaign_id):
    """
    Get the data of a campaign.
    """

    # The decorator has assured that the user had been logged in.
    # No need for checking the existence of the header at this point.
    token = flask.request.headers.get("Authorization")
    user_id = auth_service.get_user_id(token)

    # Create the DB session.
    db_session = db_access.Session()

    try:
        # Only the users who are somehow related to the campaign should be able to access its data.
        if not campaign_service.check_if_user_related_to_campaign(user_id, campaign_id):
            return _create_failure(f"Nie masz dostępu do danych kampani o ID {str(campaign_id)}."), 403

        campaign_details = campaign_service.get_campaign_details(campaign_id)

        return flask.jsonify({
            "status": "success",
            "message": "",
            "campaignDetails": campaign_details
        }), 200

    except BusinessError as err:
        db_session.rollback()

        return _create_failure(err.message), 200

    except Exception as err:
        db_session.rollback()
        logger.log_error(str(err))

        return _create_failure("Błąd aplikacji."), 500

    finally:
        db_session.close()


@MY_CAMPAIGNS_BLUEPRINT.route("/<int:campaign_id>/timeline/entry", methods=['POST'])
@allow_authorized_with_roles([ROLE_CREATE_SESSION_SUMMARY])
def my_campaigns_timeline_entry(campaign_id):
    """
    Create an entry of the campaign timeline.
    """

    token = flask.request.headers.get("Authorization")
    user_id = auth_service.get_user_id(token)
    user_name = auth_service.get_user_name(token)
    db_session = db_access.Session()

    try:
        if not campaign_service.check_if_campaign_gm(user_id, campaign_id):
            raise DomainError("User is not a GM!", "AC002", 403)

        entry_data = campaign_mapper.map_create_timeline_entry_request(flask.request.json, campaign_id)
        timeline_entry_id = campaign_service.create_timeline_entry(entry_data, user_name)
        db_session.commit()
        return flask.jsonify({
            "status": "success",
            "message": "",
            "campaignTimelineEntryId": timeline_entry_id
        })

    except DomainError as err:
        db_session.rollback()
        error_message = get_error_message(err.error_code)
        return _create_failure(error_message), err.http_status

    except Exception as err:
        db_session.rollback()
        logger.log_error(str(err))
        error_message = get_error_message("T0000")
        return _create_failure(error_message), 500

    finally:
        db_session.close()


@MY_CAMPAIGNS_BLUEPRINT.route("/<int:campaign_id>/timeline", methods=["GET"])
@allow_authorized_with_roles([ROLE_VIEW_CAMPAIGN_TIMELINE])
def my_campaigns_timeline(campaign_id):
    """
    Get the timeline of a campaign.
    """

    token = flask.request.headers.get("Authorization")
    user_id = auth_service.get_user_id(token)
    db_session = db_access.Session()

    try:
        if not campaign_service.check_if_user_related_to_campaign(user_id, campaign_id):
            raise DomainError("User is not related to the campaign!", "AC003", 403)

        timeline = campaign_service.get_timeline(campaign_id)
        return flask.jsonify({
            "status": "success",
            "message": "",
            "timeline": timeline
        })

    except DomainError as err:
        error_message = get_error_message(err.error_code)
        return _create_failure(error_message), err.http_status

    except Exception as err:
        logger.log_error(str(err))
        error_message = get_error_message("T0000")
        return _create_failure(error_message), 500

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
