"""
Application database models.

Import all SQLAlchemy models here so they are registered with
the application's metadata.

Alembic relies on these imports to detect schema changes when
generating migrations.
"""

from backend.models.conversation import Conversation
from backend.models.document import Document
from backend.models.embedding import Embedding
from backend.models.message import Message
from backend.models.settings import Settings
from backend.models.user import User


__all__ = [
    "User",
    "Document",
    "Conversation",
    "Message",
    "Embedding",
    "Settings",
]