from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.conversation import Conversation
from backend.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    """
    Repository for Conversation-specific database operations.
    """

    def __init__(self):
        super().__init__(Conversation)

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Conversation]:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
        )
        return list(result.scalars().all())

    async def get_latest(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Conversation | None:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()