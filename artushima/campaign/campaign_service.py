"""
The service module dealing with the logic behind campaigns.
"""

from artushima.campaign.persistence import campaign_repository
from artushima.core.exceptions import BusinessError
from artushima.core.utils.argument_validator import validate_int_arg
from artushima.user import user_service


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
