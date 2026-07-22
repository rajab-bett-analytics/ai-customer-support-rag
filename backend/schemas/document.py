"""
Document schemas.

Pydantic models for document-related API responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DocumentResponse(BaseModel):
    """
    Response returned after uploading a document.
    """

    id: UUID
    filename: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }