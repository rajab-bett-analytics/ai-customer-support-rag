"""
Embedding database model.

Stores document chunks together with their vector embeddings
used for semantic search in the Retrieval-Augmented Generation
(RAG) pipeline.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.base import Base
from backend.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from backend.models.document import Document


class Embedding(TimestampMixin, Base):
    """
    Represents one embedded document chunk.
    """

    __tablename__ = "embeddings"

    __table_args__ = (
        Index(
            "ix_embedding_document_page_chunk",
            "document_id",
            "page_number",
            "chunk_index",
        ),
    )

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
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Chunk Metadata
    # ---------------------------------------------------------

    page_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    section: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Vector Embedding
    # ---------------------------------------------------------

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    document: Mapped["Document"] = relationship(
        back_populates="embeddings",
        lazy="selectin",
    )