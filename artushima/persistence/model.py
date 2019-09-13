"""
The module contains the database model - the definition of entities.
"""

from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# The base class for all entities
Base = declarative_base()


class BlacklistedTokenEntity(Base):
    """
    The entity for the blacklisted token.
    """

    __tablename__ = "T_BLACKLISTED_TOKEN"

    id = Column("ID", Integer, primary_key=True)
    token = Column("TOKEN", String, nullable=False)

    def map_to_dict(self):
        """
        Map this entity data to a dictionary.
        """

        token_dto = dict()
        token_dto["id"] = self.id
        token_dto["token"] = self.token

        return token_dto


class UserEntity(Base):
    """
    The entity for the user data.
    """

    __tablename__ = "T_USER"

    id = Column("ID", Integer, primary_key=True)
    created_on = Column("CREATED_ON", DateTime, nullable=False)
    modified_on = Column("MODIFIED_ON", DateTime, nullable=False)
    opt_lock = Column("OPT_LOCK", Integer, nullable=False)
    user_name = Column("USER_NAME", String, nullable=False, unique=True)
    password_hash = Column("PASSWORD_HASH", String)
    role = Column("ROLE", Integer, nullable=False)

    user_history_entries = relationship("UserHistoryEntity", back_populates="user")
    run_campaigns = relationship("CampaignEntity", back_populates="game_master")

    def map_to_dict(self):
        """
        Map this enitity data to a dictionary.
        """

        user_dto = dict()
        user_dto["id"] = self.id
        user_dto["created_on"] = self.created_on
        user_dto["modified_on"] = self.modified_on
        user_dto["opt_lock"] = self.opt_lock
        user_dto["user_name"] = self.user_name
        user_dto["password_hash"] = self.password_hash
        user_dto["role"] = self.role

        return user_dto


class UserHistoryEntity(Base):
    """
    The entity for the history of the user entities.
    """

    __tablename__ = "T_USER_HISTORY"

    id = Column("ID", Integer, primary_key=True)
    created_on = Column("CREATED_ON", DateTime, nullable=False)
    modified_on = Column("MODIFIED_ON", DateTime, nullable=False)
    opt_lock = Column("OPT_LOCK", Integer, nullable=False)
    editor_name = Column("EDITOR_NAME", String, nullable=False)
    message = Column("MESSAGE", String, nullable=False)
    user_id = Column("USER_ID", Integer, ForeignKey("T_USER.ID"), nullable=False)

    user = relationship("UserEntity", back_populates="user_history_entries")

    def map_to_dict(self):
        """
        Map this enitity data to a dictionary.
        """

        user_history_dto = dict()
        user_history_dto["id"] = self.id
        user_history_dto["created_on"] = self.created_on
        user_history_dto["modified_on"] = self.modified_on
        user_history_dto["opt_lock"] = self.opt_lock
        user_history_dto["editor_name"] = self.editor_name
        user_history_dto["message"] = self.message
        user_history_dto["user_id"] = self.user_id

        return user_history_dto


class CampaignEntity(Base):
    """
    The entity for the campaign data.
    """

    __tablename__ = "T_CAMPAIGN"

    id = Column("ID", Integer, primary_key=True)
    created_on = Column("CREATED_ON", DateTime, nullable=False)
    modified_on = Column("MODIFIED_ON", DateTime, nullable=False)
    opt_lock = Column("OPT_LOCK", Integer, nullable=False)
    name = Column("NAME", String, nullable=False)
    start_date = Column("START_DATE", Date, nullable=False)
    current_day = Column("CURRENT_DAY", Integer, nullable=False)
    game_master_id = Column("GAME_MASTER_ID", Integer, ForeignKey("T_USER.ID"), nullable=False)
    running = Column("RUNNING", Boolean, nullable=False)

    campaign_history_entries = relationship("CampaignHistoryEntity", back_populates="campaign")
    game_master = relationship("UserEntity", back_populates="run_campaigns")

    def map_to_dict(self):
        """
        Map this enitity data to a dictionary.
        """

        campaign_dto = dict()
        campaign_dto["id"] = self.id
        campaign_dto["created_on"] = self.created_on
        campaign_dto["modified_on"] = self.modified_on
        campaign_dto["opt_lock"] = self.opt_lock
        campaign_dto["name"] = self.name
        campaign_dto["start_date"] = self.start_date
        campaign_dto["current_day"] = self.current_day
        campaign_dto["game_master_id"] = self.game_master_id
        campaign_dto["running"] = self.running

        return campaign_dto


class CampaignHistoryEntity(Base):
    """
    The entity for the history of campaign entities.
    """

    __tablename__ = "T_CAMPAIGN_HISTORY"

    id = Column("ID", Integer, primary_key=True)
    created_on = Column("CREATED_ON", DateTime, nullable=False)
    modified_on = Column("MODIFIED_ON", DateTime, nullable=False)
    opt_lock = Column("OPT_LOCK", Integer, nullable=False)
    editor_name = Column("EDITOR_NAME", String, nullable=False)
    message = Column("MESSAGE", String, nullable=False)
    campaign_id = Column("CAMPAIGN_ID", Integer, ForeignKey("T_CAMPAIGN.ID"), nullable=False)

    campaign = relationship("CampaignEntity", back_populates="campaign_history_entries")

    def map_to_dict(self):
        """
        Map this enitity data to a dictionary.
        """

        campaign_history_dto = dict()
        campaign_history_dto["id"] = self.id
        campaign_history_dto["created_on"] = self.created_on
        campaign_history_dto["modified_on"] = self.modified_on
        campaign_history_dto["opt_lock"] = self.opt_lock
        campaign_history_dto["editor_name"] = self.editor_name
        campaign_history_dto["message"] = self.message
        campaign_history_dto["campaign_id"] = self.campaign_id

        return campaign_history_dto
