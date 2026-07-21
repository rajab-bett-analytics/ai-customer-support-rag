"""
Application configuration.

This module is the single source of truth for all application
configuration. It loads environment variables from the project's
.env file and exposes them through a validated Settings object.

No other module should read environment variables directly.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Every setting in this class is automatically loaded from the
    project's .env file.
    """

    # ---------------------------------------------------------
    # Application Settings
    # ---------------------------------------------------------

    APP_NAME: str = "AI Customer Support RAG API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ---------------------------------------------------------
    # Database Settings
    # ---------------------------------------------------------

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ---------------------------------------------------------
    # Authentication Settings
    # ---------------------------------------------------------

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ---------------------------------------------------------
    # AI Provider
    # ---------------------------------------------------------

    OPENAI_API_KEY: str = ""

    # ---------------------------------------------------------
    # Async Database URL (FastAPI)
    # ---------------------------------------------------------

    @property
    def DATABASE_URL(self) -> str:
        """
        Build the asynchronous PostgreSQL connection URL.

        Used by FastAPI and SQLAlchemy AsyncSession.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # ---------------------------------------------------------
    # Sync Database URL (Alembic)
    # ---------------------------------------------------------

    @property
    def ALEMBIC_DATABASE_URL(self) -> str:
        """
        Build the synchronous PostgreSQL connection URL.

        Used exclusively by Alembic migrations.
        """
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # ---------------------------------------------------------
    # Pydantic Settings Configuration
    # ---------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# ---------------------------------------------------------
# Global Settings Instance
# ---------------------------------------------------------

settings = Settings()