"""
Database configuration.

This module creates the SQLAlchemy asynchronous engine and
session factory used throughout the application.

All database interactions should obtain an AsyncSession
from the get_db() dependency defined here.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import settings

# ---------------------------------------------------------
# SQLAlchemy Async Engine
#
# The engine manages the application's connection pool
# and communicates asynchronously with PostgreSQL.
# ---------------------------------------------------------

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# ---------------------------------------------------------
# Async Session Factory
#
# Creates a new AsyncSession for each request.
# ---------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# ---------------------------------------------------------
# Database Dependency
#
# FastAPI injects an AsyncSession into endpoints that
# depend on get_db().
# ---------------------------------------------------------


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    A new session is created for each request and is
    automatically closed when the request finishes.

    Yields:
        AsyncSession: SQLAlchemy asynchronous session.
    """

    async with AsyncSessionLocal() as session:
        yield session