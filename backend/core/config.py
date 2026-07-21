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
    # Database
    # ---------------------------------------------------------

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ---------------------------------------------------------
    # AI Provider
    # ---------------------------------------------------------

    OPENAI_API_KEY: str = ""
    
    
        # ---------------------------------------------------------
    # Computed Database URL
    # ---------------------------------------------------------

    @property
    def DATABASE_URL(self) -> str:
        """
        Build the SQLAlchemy PostgreSQL connection URL.

        Returns:
            A PostgreSQL connection string compatible with SQLAlchemy.
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
    # Pydantic Settings Configuration
    # ---------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# ---------------------------------------------------------
# Global settings instance
#
# Import this object anywhere in the application:
#
# from backend.core.config import settings
# ---------------------------------------------------------

settings = Settings()