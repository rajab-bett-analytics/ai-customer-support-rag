"""
Authentication schemas.

These schemas define the request and response models used
for JWT authentication.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Response returned after successful authentication.
    """

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    JWT payload after decoding.
    """

    sub: str