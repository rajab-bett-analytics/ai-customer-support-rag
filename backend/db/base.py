"""
Database base class.

This module defines the declarative base that all SQLAlchemy
ORM models inherit from.

Keeping the Base in a dedicated module allows every model
to share the same metadata, which is required for migrations
and table creation.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every database model should inherit from this class.
    """

    pass