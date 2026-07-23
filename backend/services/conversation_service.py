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
    Handles conversation management.
    """

    def __init__(self) -> None:
        self.conversation_repository = ConversationRepository()
        self.message_repository = MessageRepository()

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
            db,
            conversation,
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
            db,
            conversation_id,
        )

    async def get_latest_conversation(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Conversation | None:
        """
        Retrieve the user's most recent conversation.
        """

        return await self.conversation_repository.get_latest(
            db,
            user_id,
        )

    async def save_message(
        self,
        db: AsyncSession,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Save a message to a conversation.
        """

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        return await self.message_repository.create_message(
            db,
            message,
        )

    async def get_messages(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> list[Message]:
        """
        Retrieve all messages belonging to a conversation.
        """

        return await self.message_repository.get_by_conversation(
            db,
            conversation_id,
        )

    async def get_history(
        self,
        db: AsyncSession,
        conversation_id: int,
    ) -> str:
        """
        Build a formatted conversation history for the LLM.

        Args:
            db: Database session.
            conversation_id: Conversation identifier.

        Returns:
            Conversation history formatted as dialogue.
        """

        messages = await self.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        if not messages:
            return ""

        history: list[str] = []

        for message in messages:
            history.append(
                f"{message.role.title()}: {message.content}"
            )

        return "\n".join(history)