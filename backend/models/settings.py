"""
Application settings model.

Stores user-specific AI configuration.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Float,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.base import Base
from backend.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from backend.models.user import User


class Settings(
    TimestampMixin,
    Base,
):

    __tablename__ = "settings"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True,
    )


    ai_provider: Mapped[str] = mapped_column(
        String(50),
        default="Google Gemini",
        nullable=False,
    )


    chat_model: Mapped[str] = mapped_column(
        String(100),
        default="gemini-2.5-flash",
        nullable=False,
    )


    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="gemini-embedding-001",
        nullable=False,
    )


    top_k: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )


    similarity_threshold: Mapped[float] = mapped_column(
        Float,
        default=0.75,
        nullable=False,
    )


    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.2,
        nullable=False,
    )


    max_tokens: Mapped[int] = mapped_column(
        Integer,
        default=2048,
        nullable=False,
    )


    system_prompt: Mapped[str] = mapped_column(
        String(4000),
        default="You are a helpful AI assistant.",
        nullable=False,
    )


    user: Mapped["User"] = relationship(
        back_populates="settings",
    )