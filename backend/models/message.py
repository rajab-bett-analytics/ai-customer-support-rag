"""
Message database model.

Stores individual messages exchanged between a user
and the AI assistant.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from backend.models.mixins import TimestampMixin
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.conversation import Conversation


class Message(TimestampMixin, Base):
    """
    Represents a single chat message.
    """

    __tablename__ = "messages"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ---------------------------------------------------------
    # Conversation
    # ---------------------------------------------------------

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Message Information
    # ---------------------------------------------------------

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )