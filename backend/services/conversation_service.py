"""
Conversation service.

Handles conversation management and message persistence.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.repositories.conversation_repository import (
    ConversationRepository,
)
from backend.repositories.message_repository import (
    MessageRepository,
)


class ConversationService:
    """
    Handles conversation lifecycle and message history.
    """

    MAX_HISTORY_MESSAGES = 20

    def __init__(self) -> None:
        self.conversation_repository = (
            ConversationRepository()
        )
        self.message_repository = (
            MessageRepository()
        )

    async def create_conversation(
        self,
        db: AsyncSession,
        user_id: int,
        title: str = "New Conversation",
    ) -> Conversation:
        """
        Create a new conversation.
        """

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        return await self.conversation_repository.create(
            db=db,
            conversation=conversation,
        )

    async def get_conversation(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve a conversation by ID.
        """

        return await self.conversation_repository.get_by_id(
            db=db,
            conversation_id=conversation_id,
        )

    async def get_user_conversations(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[Conversation]:
        """
        Retrieve all conversations for a user.
        """

        return await self.conversation_repository.get_by_user(
            db=db,
            user_id=user_id,
        )

    async def get_latest_conversation(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Conversation | None:
        """
        Retrieve the user's latest conversation.
        """

        return await self.conversation_repository.get_latest(
            db=db,
            user_id=user_id,
        )

    async def delete_conversation(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> None:
        """
        Delete a conversation.
        """

        await self.conversation_repository.delete(
            db=db,
            conversation_id=conversation_id,
        )

    async def save_message(
        self,
        db: AsyncSession,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Persist a conversation message.
        """

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content.strip(),
        )

        return await self.message_repository.create_message(
            db=db,
            message=message,
        )

    async def get_messages(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> list[Message]:
        """
        Retrieve messages for a conversation.
        """

        return await self.message_repository.get_by_conversation(
            db=db,
            conversation_id=conversation_id,
        )

    async def get_history(
        self,
        db: AsyncSession,
        conversation_id: int,
        max_messages: int | None = None,
    ) -> str:
        """
        Build formatted conversation history for the AI.
        """

        messages = await self.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        if not messages:
            return ""

        limit = (
            max_messages
            if max_messages is not None
            else self.MAX_HISTORY_MESSAGES
        )

        messages = messages[-limit:]

        history: list[str] = []

        for message in messages:

            role = (
                "Assistant"
                if message.role == "assistant"
                else "User"
            )

            history.append(
                f"{role}: {message.content.strip()}"
            )

        return "\n".join(history)