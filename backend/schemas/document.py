"""
Document schemas.

Pydantic models for document-related API responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """
    Document returned to the frontend.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id: int

    # ---------------------------------------------------------
    # File Information
    # ---------------------------------------------------------

    filename: str
    stored_filename: str

    mime_type: str
    file_size: int

    # ---------------------------------------------------------
    # Processing Information
    # ---------------------------------------------------------

    status: str

    page_count: int
    chunk_count: int
    embedding_count: int

    indexed_at: datetime | None = None

    error_message: str | None = None

    # ---------------------------------------------------------
    # Ownership
    # ---------------------------------------------------------

    uploaded_by: int

    # ---------------------------------------------------------
    # Timestamps
    # ---------------------------------------------------------

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )