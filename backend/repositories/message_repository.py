from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.message import Message
from backend.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """
    Repository for Message-specific database operations.
    """

    def __init__(self):
        super().__init__(Message)

    async def get_by_conversation(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> list[Message]:
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(asc(Message.created_at))
        )
        return list(result.scalars().all())