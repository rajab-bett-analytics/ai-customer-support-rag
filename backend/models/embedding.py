"""
Embedding database model.

Stores document chunks and their vector embeddings used
for semantic search in the RAG pipeline.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from backend.models.mixins import TimestampMixin
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.document import Document


class Embedding(TimestampMixin, Base):
    """
    Represents a chunk of a document.
    """

    __tablename__ = "embeddings"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ---------------------------------------------------------
    # Parent Document
    # ---------------------------------------------------------

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Chunk Information
    # ---------------------------------------------------------

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------

    document: Mapped["Document"] = relationship(
        back_populates="embeddings",
    )