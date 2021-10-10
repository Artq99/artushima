"""
The service module dealing with the logic behind campaigns.
"""

from datetime import datetime, timedelta

from artushima.campaign import campaign_mapper
from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import (CampaignEntity,
                                                  CampaignHistoryEntity)
from artushima.core.exceptions import BusinessError, DomainError
from artushima.core.history_messages import get_message
from artushima.core.utils.argument_validator import (assert_int,
                                                     validate_int_arg)
from artushima.user import user_service


def create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id, game_master_name):
    """
    Create a new campaign.
    """

    # Saving the timestamp so all entities can share the same time of creation.
    timestamp = datetime.utcnow()

    # Creating the campaign.
    campaign = _create_campaign_entity(timestamp, campaign_name, begin_date, passed_days, game_master_id)

    # Adding history entry about creation.
    creation_history_entry_message = f"Kampania {campaign_name} została utworzona."
    _add_history_entry_to_campaign(campaign, editor_name, timestamp, creation_history_entry_message)

    # Adding history entry about the current game master.
    gm_history_entry_message = f"Obecnym mistrzem gry zostaje {game_master_name}."
    _add_history_entry_to_campaign(campaign, editor_name, timestamp, gm_history_entry_message)

    # Persisting.
    campaign_repository.persist(campaign)


def _create_campaign_entity(timestamp, campaign_name, begin_date, passed_days, game_master_id):
    """
    Create a new instance of the campaign entity with the given data.
    """

    campaign_entity = CampaignEntity()
    campaign_entity.created_on = timestamp
    campaign_entity.modified_on = timestamp
    campaign_entity.opt_lock = 0
    campaign_entity.campaign_name = campaign_name
    campaign_entity.begin_date = begin_date
    campaign_entity.passed_days = passed_days
    campaign_entity.game_master_id = game_master_id
    return campaign_entity


def _add_history_entry_to_campaign(campaign, editor_name, timestamp, message):
    """
    Add a new history entry to the given campaign.
    """

    campaign_history_entry = CampaignHistoryEntity()
    campaign_history_entry.created_on = timestamp
    campaign_history_entry.modified_on = timestamp
    campaign_history_entry.opt_lock = 0
    campaign_history_entry.editor_name = editor_name
    campaign_history_entry.message = message
    campaign.campaign_history_entries.append(campaign_history_entry)


def get_campaigns_by_gm_id(gm_id):
    """
    Get the campaigns belonging to the game master of the given ID.
    """

    validate_int_arg(gm_id, "ID mistrza gry")

    if user_service.get_user_by_id(gm_id) is None:
        raise BusinessError(f"Użytkownik o ID {gm_id} nie istnieje!")

    campaigns = campaign_repository.read_by_gm_id(gm_id)

    result = list()

    for campaign in campaigns:
        result.append(_map_campaign_to_dict(campaign))

    return result


def _map_campaign_to_dict(campaign):
    return {
        "id": campaign.id,
        "created_on": campaign.created_on,
        "modified_on": campaign.modified_on,
        "opt_lock": campaign.opt_lock,
        "campaign_name": campaign.campaign_name,
        "begin_date": campaign.begin_date,
        "passed_days": campaign.passed_days,
    }


def get_campaign_details(campaign_id):
    """
    Get the details of a campaign.
    """

    validate_int_arg(campaign_id, "ID kampanii")

    campaign = campaign_repository.read_by_id(campaign_id)
    if campaign is None:
        raise BusinessError(f"Kampania o ID {campaign_id} nie istnieje!")

    current_date = campaign.begin_date + timedelta(days=campaign.passed_days)

    return {
        "id": campaign.id,
        "title": campaign.campaign_name,
        "creationDate": campaign.created_on.isoformat(),
        "startDate": campaign.begin_date.isoformat(),
        "passedDays": campaign.passed_days,
        "currentDate": current_date.isoformat(),
        "gameMasterId": campaign.game_master.id,
        "gameMasterName": campaign.game_master.user_name
    }


def create_timeline_entry(entry_data: dict, editor_name: str) -> int:
    """
    Create an entry in the timeline of a campaign.
    """

    campaign = campaign_repository.read_by_id(entry_data["campaignId"])

    if campaign is None:
        raise DomainError("Campaign does not extist!", "DC002")

    timestamp = datetime.utcnow()
    timeline_entry = campaign_mapper.map_timeline_entry_data_to_timeline_entity(entry_data, timestamp)
    campaign.campaign_timeline_entries.append(timeline_entry)

    history_entry_data = {
        "editorName": editor_name,
        "message": get_message("campaign: timeline entry created").format(entry_data["title"])
    }
    history_entry = campaign_mapper.map_history_entry_data_to_history_entity(history_entry_data, timestamp)
    campaign.campaign_history_entries.append(history_entry)

    campaign_repository.persist(campaign)

    return timeline_entry.id


def get_timeline(campaign_id):
    """
    Get the timeline of a campaign.
    """

    assert_int(campaign_id, "DC001")

    campaign = campaign_repository.read_by_id(campaign_id)
    if campaign is None:
        raise DomainError("Campaign does not exist!", "DC002")

    timeline = []
    for entry in campaign.campaign_timeline_entries:
        mapped_entry = campaign_mapper.map_campaign_timeline_entity_to_dict(entry)
        timeline.append(mapped_entry)

    return timeline


def check_if_campaign_gm(user_id, campaign_id):
    """
    Check if the user of the given ID is the game master of the campaign of the given ID.
    """

    assert_int(user_id, "DU001")
    assert_int(campaign_id, "DC001")

    campaign = campaign_repository.read_by_id(campaign_id)

    if campaign is None:
        raise DomainError("Campaign does not exist!", "DC002")

    return campaign.game_master.id == user_id


def check_if_user_related_to_campaign(user_id, campaign_id):
    """
    Check if the user of the given ID is somehow related to the campaign
    of the given ID, i.e. if he/she is its game master or participates
    as a player.

    TODO For now only game masters are checked.
    """

    validate_int_arg(user_id, "ID użytkownika")
    validate_int_arg(campaign_id, "ID kampanii")

    campaign = campaign_repository.read_by_id(campaign_id)

    if campaign is None:
        raise BusinessError(f"Kampania o ID {campaign_id} nie istnieje!")

    return campaign.game_master.id == user_id
