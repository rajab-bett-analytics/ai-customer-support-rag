"""
Document database model.

Stores uploaded knowledge base documents used by the
Retrieval-Augmented Generation (RAG) pipeline.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base
from backend.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from backend.models.embedding import Embedding
    from backend.models.user import User


class Document(TimestampMixin, Base):
    """
    Represents an uploaded knowledge base document.
    """

    __tablename__ = "documents"

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

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Original Document Information
    # ---------------------------------------------------------

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        nullable=False,
    )

    # ---------------------------------------------------------
    # Processing Status
    # ---------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="uploaded",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    owner: Mapped["User"] = relationship(
        back_populates="documents",
    )

    embeddings: Mapped[list["Embedding"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )