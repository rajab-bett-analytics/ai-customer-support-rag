"""
User schemas.

This module defines the request and response models used
for user registration, authentication, and API responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for user registration.
    """

    full_name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100,
        ),
    ]

    email: EmailStr

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
        ),
    ]


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
        ),
    ]


class UserResponse(BaseModel):
    """
    Schema returned to API clients.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime