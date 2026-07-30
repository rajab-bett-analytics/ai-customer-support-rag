"""
Retrieval schemas.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pydantic import BaseModel


class CitationResponse(BaseModel):
    """
    Metadata describing the origin of a retrieved chunk.
    """

    document_id: int

    filename: str

    page: int | None

    section: str | None

    chunk_index: int


class RetrievalResponse(BaseModel):
    """
    Result returned by the retrieval service.
    """

    context: str

    citations: list[CitationResponse]