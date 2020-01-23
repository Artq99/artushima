"""
The module containing the data model for the auth component.
"""

from sqlalchemy import Column, Integer, String

from artushima.core.db_access import BaseEntity


class BlacklistedTokenEntity(BaseEntity):
    """
    The entity for the blacklisted token.
    """

    __tablename__ = "blacklisted_token"

    id = Column("ID", Integer, primary_key=True)
    token = Column("TOKEN", String(255), nullable=False)
