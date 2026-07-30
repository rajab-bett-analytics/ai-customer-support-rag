"""
Alembic environment configuration.

This module configures Alembic for managing database schema
migrations. Alembic uses a synchronous SQLAlchemy engine,
while the FastAPI application uses an asynchronous engine.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from backend.core.config import settings
from backend.db.base import Base

# Import all models so Alembic can discover them
import backend.models  # noqa: F401


# ---------------------------------------------------------
# Alembic Configuration
# ---------------------------------------------------------

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.ALEMBIC_DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline Migrations
# ---------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations without connecting to the database.
    """

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online Migrations
# ---------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations while connected to the database.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()