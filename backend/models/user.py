"""
User database model.

This module defines the User table used for authentication
and ownership of application resources.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.mixins import TimestampMixin
from backend.db.base import Base


if TYPE_CHECKING:
    from backend.models.conversation import Conversation
    from backend.models.document import Document


class User(TimestampMixin,Base):
    """
    Represents an application user.
    """

    __tablename__ = "users"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ---------------------------------------------------------
    # User Information
    # ---------------------------------------------------------

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    documents: Mapped[list["Document"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )