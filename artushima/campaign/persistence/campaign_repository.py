"""
The repository module providing access to the data related to the campaign
entity.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from artushima.core import db_access
from artushima.core.exceptions import PersistenceError
from artushima.campaign.persistence.model import CampaignEntity


def persist(campaign):
    """
    Persist the campaign data.
    """

    if not isinstance(campaign, CampaignEntity):
        raise ValueError("The argument is not CampaignEntity!")

    try:
        session: Session = db_access.Session()
        session.add(campaign)
        session.flush()
        return campaign
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on persisting a campaign: {str(err)}")


def read_by_gm_id(gm_id):
    """
    Get all campaigns belonging to the game master of the given ID.
    """

    try:
        session: Session = db_access.Session()
        return session.query(CampaignEntity).filter_by(game_master_id=gm_id).all()
    except SQLAlchemyError as err:
        raise PersistenceError(f"Error on reading campaigns of the GM (ID: {str(gm_id)}): {str(err)}") from err
