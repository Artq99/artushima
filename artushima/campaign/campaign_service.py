"""
The service module dealing with the logic behind campaigns.
"""

from datetime import date, datetime

from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import CampaignEntity, CampaignHistoryEntity
from artushima.core.exceptions import BusinessError
from artushima.core.utils.argument_validator import validate_int_arg
from artushima.user import user_service


def create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id):
    """
    Create a new campaign.
    """

    _validate_arguments_for_creation(editor_name, campaign_name, begin_date, passed_days, game_master_id)
    timestamp = datetime.utcnow()
    campaign = _create_campaign_entity(timestamp, campaign_name, begin_date, passed_days, game_master_id)
    _create_and_assign_history_entry_creation(campaign, timestamp, editor_name)
    campaign_repository.persist(campaign)


def _validate_arguments_for_creation(editor_name, campaign_name, begin_date, passed_days, game_master_id):
    if editor_name is None:
        raise ValueError("editor_name cannot be None")

    if not isinstance(editor_name, str):
        raise TypeError(f"editor_name must be str, not {type(editor_name).__name__}")

    if not editor_name:
        raise ValueError("editor_name cannot be empty")

    if campaign_name is None:
        raise ValueError("campaign_name cannot be None")

    if not isinstance(campaign_name, str):
        raise TypeError(f"campaign_name must be str, not {type(campaign_name).__name__}")

    if not campaign_name:
        raise ValueError("campaign_name cannot be empty")

    if begin_date is None:
        raise ValueError("begin_date cannot be None")

    if not isinstance(begin_date, date):
        raise TypeError(f"begin_date must be date, not {type(begin_date).__name__}")

    if passed_days is None:
        raise ValueError("passed_days cannot be None")

    if not isinstance(passed_days, int):
        raise TypeError(f"passed_days must be int, not {type(passed_days).__name__}")

    if game_master_id is None:
        raise ValueError("game_master_id cannot be None")

    if not isinstance(game_master_id, int):
        raise TypeError(f"game_master_id must be int, not {type(passed_days).__name__}")


def _create_campaign_entity(timestamp, campaign_name, begin_date, passed_days, game_master_id):
    campaign_entity = CampaignEntity()
    campaign_entity.created_on = timestamp
    campaign_entity.modified_on = timestamp
    campaign_entity.opt_lock = 0
    campaign_entity.campaign_name = campaign_name
    campaign_entity.begin_date = begin_date
    campaign_entity.passed_days = passed_days
    campaign_entity.game_master_id = game_master_id

    return campaign_entity


def _create_and_assign_history_entry_creation(campaign, timestamp, editor_name):
    campaign_history_entry = CampaignHistoryEntity()
    campaign_history_entry.created_on = timestamp
    campaign_history_entry.modified_on = timestamp
    campaign_history_entry.opt_lock = 0
    campaign_history_entry.editor_name = editor_name
    campaign_history_entry.message = f"Kampania {campaign.campaign_name} została utworzona."

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
