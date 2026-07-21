"""
Database configuration.

This module creates the SQLAlchemy engine and session factory
used throughout the application.

All database interactions should obtain a session from the
get_db() dependency defined here.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.core.config import settings

# ---------------------------------------------------------
# SQLAlchemy Engine
#
# The engine manages the application's connection pool
# and communicates with the PostgreSQL database.
# ---------------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# ---------------------------------------------------------
# Session Factory
#
# Creates new database sessions for each request.
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------
# Database Dependency
#
# FastAPI will inject a database session into endpoints
# that depend on get_db().
# ---------------------------------------------------------


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session.

    A new session is created for each request and is
    automatically closed when the request finishes.

    Yields:
        Session: SQLAlchemy database session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()