"""
The module containing the data model for the campaign component.
"""

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from artushima.core.db_access import BaseEntity


class CampaignEntity(BaseEntity):
    """
    The entity for the campaign data.
    """

    __tablename__ = "campaign"

    id = Column("id", Integer, primary_key=True)
    created_on = Column("created_on", DateTime, nullable=False)
    modified_on = Column("modified_on", DateTime, nullable=False)
    opt_lock = Column("opt_lock", Integer, nullable=False)
    campaign_name = Column("campaign_name", String(255), nullable=False)
    begin_date = Column("begin_date", Date, nullable=False)
    passed_days = Column("passed_days", Integer, nullable=False)
    game_master_id = Column("game_master_id", Integer, ForeignKey("user.id"), nullable=False)

    campaign_history_entries = relationship("CampaignHistoryEntity", back_populates="campaign")
    game_master = relationship("UserEntity", back_populates="owned_campaigns")


class CampaignHistoryEntity(BaseEntity):
    """
    The entity for the history of the campaign entities.
    """

    __tablename__ = "campaign_history"

    id = Column("id", Integer, primary_key=True)
    created_on = Column("created_on", DateTime, nullable=False)
    modified_on = Column("modified_on", DateTime, nullable=False)
    opt_lock = Column("opt_lock", Integer, nullable=False)
    editor_name = Column("editor_name", String, nullable=False)
    message = Column("message", String(255), nullable=False)
    campaign_id = Column("campaign_id", Integer, ForeignKey("campaign.id"), nullable=False)

    campaign = relationship("CampaignEntity", back_populates="campaign_history_entries")
