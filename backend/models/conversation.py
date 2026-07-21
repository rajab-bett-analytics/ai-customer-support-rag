"""
Conversation database model.

Represents a chat session between a user and the AI assistant.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations
from backend.models.mixins import TimestampMixin
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.message import Message
    from backend.models.user import User

class Conversation(TimestampMixin, Base):
    """
    Represents a conversation between a user and the AI assistant.
    """

    __tablename__ = "conversations"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ---------------------------------------------------------
    # Ownership
    # ---------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Conversation Information
    # ---------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    user: Mapped["User"] = relationship(
        back_populates="conversations",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )