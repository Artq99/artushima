"""
The service module dealing with the logic behind campaigns.
"""

from datetime import datetime

from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import (CampaignEntity,
                                                  CampaignHistoryEntity)
from artushima.core.exceptions import BusinessError
from artushima.core.utils.argument_validator import validate_int_arg
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
