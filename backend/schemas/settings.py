"""
Application settings schemas.

Defines request and response models for per-user
AI Customer Support Platform settings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class SettingsUpdate(BaseModel):
    """
    Schema used to update user settings.
    """

    ai_provider: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
        ),
    ]

    chat_model: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100,
        ),
    ]

    embedding_model: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100,
        ),
    ]

    top_k: Annotated[
        int,
        Field(
            ge=1,
            le=20,
        ),
    ]

    similarity_threshold: Annotated[
        float,
        Field(
            ge=0.0,
            le=1.0,
        ),
    ]

    temperature: Annotated[
        float,
        Field(
            ge=0.0,
            le=2.0,
        ),
    ]

    max_tokens: Annotated[
        int,
        Field(
            ge=256,
            le=8192,
        ),
    ]

    system_prompt: Annotated[
        str,
        Field(
            min_length=10,
            max_length=4000,
        ),
    ]


class SettingsResponse(BaseModel):
    """
    Schema returned to API clients.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    ai_provider: str

    chat_model: str

    embedding_model: str

    top_k: int

    similarity_threshold: float

    temperature: float

    max_tokens: int

    system_prompt: str

    created_at: datetime

    updated_at: datetime