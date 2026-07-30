"""
Repository for application settings.

Handles database operations for user-specific
application settings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.settings import Settings
from backend.repositories.base import BaseRepository


class SettingsRepository(
    BaseRepository[Settings],
):
    """
    Repository for user application settings.
    """

    def __init__(self) -> None:
        super().__init__(Settings)


    async def get_by_user_id(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Settings | None:
        """
        Retrieve settings belonging to a specific user.
        """

        result = await db.execute(
            select(Settings).where(
                Settings.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()


    async def create_default_settings(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Settings:
        """
        Create default settings for a user.
        """

        settings = Settings(
            user_id=user_id,
        )

        return await self.create(
            db,
            settings,
        )