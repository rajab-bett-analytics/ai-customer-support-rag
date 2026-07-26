"""
Message repository.

Provides database operations for conversation messages.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.message import Message
from backend.repositories.base import BaseRepository


class MessageRepository(
    BaseRepository[Message]
):
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
        Retrieve all messages for a conversation.
        """

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                asc(Message.created_at)
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_latest_message(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> Message | None:
        """
        Retrieve the latest message in a conversation.
        """

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                desc(Message.created_at)
            )
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def count_messages(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> int:
        """
        Count messages in a conversation.
        """

        result = await db.execute(
            select(
                func.count(Message.id)
            ).where(
                Message.conversation_id
                == conversation_id
            )
        )

        return int(
            result.scalar_one()
        )

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

    async def delete_by_conversation(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> None:
        """
        Delete every message belonging to a conversation.
        """

        messages = await self.get_by_conversation(
            db=db,
            conversation_id=conversation_id,
        )

        for message in messages:
            await db.delete(message)

        await db.commit()