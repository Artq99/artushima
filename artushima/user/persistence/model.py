"""
The module containing the data model for the user component.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from artushima.core.db_access import BaseEntity


class UserEntity(BaseEntity):
    """
    The entity for the user data.
    """

    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    created_on = Column("created_on", DateTime, nullable=False)
    modified_on = Column("modified_on", DateTime, nullable=False)
    opt_lock = Column("opt_lock", Integer, nullable=False)
    user_name = Column("user_name", String(255), nullable=False, unique=True)
    password_hash = Column("password_hash", String(255))

    user_history_entries = relationship("UserHistoryEntity", back_populates="user")
    user_roles = relationship("UserRoleEntity", back_populates="user")


class UserHistoryEntity(BaseEntity):
    """
    The entity for the history of the user entities.
    """

    __tablename__ = "user_history"

    id = Column("id", Integer, primary_key=True)
    created_on = Column("created_on", DateTime, nullable=False)
    modified_on = Column("modified_on", DateTime, nullable=False)
    opt_lock = Column("opt_lock", Integer, nullable=False)
    editor_name = Column("editor_name", String, nullable=False)
    message = Column("message", String(255), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("UserEntity", back_populates="user_history_entries")


class UserRoleEntity(BaseEntity):
    """
    The entity for user roles.
    """

    __tablename__ = "user_role"

    id = Column("id", Integer, primary_key=True)
    created_on = Column("created_on", DateTime, nullable=False)
    modified_on = Column("modified_on", DateTime, nullable=False)
    opt_lock = Column("opt_lock", Integer, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("user.id"), nullable=False)
    role_name = Column("role_name", String(255), nullable=False)

    user = relationship("UserEntity", back_populates="user_roles")
