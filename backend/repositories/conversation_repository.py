"""
Conversation repository.

Provides database operations for conversations and messages.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    """
    Repository for conversation-specific database operations.
    """

    def __init__(self) -> None:
        super().__init__(Conversation)

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Conversation]:
        """
        Retrieve all conversations belonging to a user.
        """

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
        """
        Retrieve the user's most recent conversation.
        """

        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its ID.
        """

        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none()

    async def add_message(
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

    async def get_messages(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> list[Message]:
        """
        Retrieve all messages for a conversation.
        """

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at)
        )

        return list(result.scalars().all())