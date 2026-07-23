"""
Message repository.

Provides database operations for conversation messages.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.message import Message
from backend.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """
    Repository for message-specific database operations.
    """

    def __init__(self) -> None:
        super().__init__(Message)

    async def get_by_conversation(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> list[Message]:
        """
        Retrieve all messages belonging to a conversation.
        """

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(asc(Message.created_at))
        )

        return list(result.scalars().all())

    async def create_message(
        self,
        db: AsyncSession,
        message: Message,
    ) -> Message:
        """
        Persist a conversation message.
        """

        db.add(message)

        await db.commit()

        await db.refresh(message)

        return message