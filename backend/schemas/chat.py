"""
Chat schemas.

Defines request and response models for the chat endpoint.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request body for asking a question.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User question.",
    )

    conversation_id: int | None = Field(
        default=None,
        description=(
            "Existing conversation ID. Leave empty to "
            "start a new conversation."
        ),
    )


class SourceResponse(BaseModel):
    """
    Source document used to generate the answer.
    """

    document_id: int

    document_name: str

    document_url: str

    page: int | None = None

    chunk_index: int

    section: str | None = None

    chunk_text: str | None = None


class ChatResponse(BaseModel):
    """
    Response returned by the chat endpoint.
    """

    conversation_id: int

    question: str

    answer: str

    sources: list[SourceResponse]