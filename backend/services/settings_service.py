"""
Application settings service.

Contains the business logic for managing
user-specific application settings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.settings import Settings
from backend.models.user import User

from backend.repositories.settings_repository import (
    SettingsRepository,
)

from backend.schemas.settings import (
    SettingsUpdate,
)


class SettingsService:
    """
    Service for user application settings.
    """

    def __init__(self) -> None:
        self.repository = SettingsRepository()


    async def get_settings(
        self,
        db: AsyncSession,
        user: User,
    ) -> Settings:
        """
        Retrieve settings for the current user.

        Creates default settings if none exist.
        """

        settings = await self.repository.get_by_user_id(
            db,
            user.id,
        )


        if settings is None:
            settings = (
                await self.repository.create_default_settings(
                    db,
                    user.id,
                )
            )


        return settings


    async def update_settings(
        self,
        db: AsyncSession,
        user: User,
        settings_data: SettingsUpdate,
    ) -> Settings:
        """
        Update settings for the current user.
        """

        settings = await self.get_settings(
            db,
            user,
        )


        settings.ai_provider = (
            settings_data.ai_provider
        )

        settings.chat_model = (
            settings_data.chat_model
        )

        settings.embedding_model = (
            settings_data.embedding_model
        )

        settings.top_k = (
            settings_data.top_k
        )

        settings.similarity_threshold = (
            settings_data.similarity_threshold
        )

        settings.temperature = (
            settings_data.temperature
        )

        settings.max_tokens = (
            settings_data.max_tokens
        )

        settings.system_prompt = (
            settings_data.system_prompt
        )


        return await self.repository.update(
            db,
            settings,
        )