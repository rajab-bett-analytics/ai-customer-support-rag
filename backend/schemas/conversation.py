"""
Conversation schemas.

Defines request and response models for conversation APIs.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from datetime import datetime

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    Represents a single chat message.
    """

    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    """
    Summary of a conversation.
    """

    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """
    Full conversation including all messages.
    """

    id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse]