"""
Analytics repository.

Provides user-specific analytics database operations.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.conversation import Conversation
from backend.models.document import Document
from backend.models.message import Message


class AnalyticsRepository:
    """
    Handles analytics database queries.
    """

    async def get_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> dict:
        """
        Return analytics for a specific user.
        """

        # ---------------------------------------------
        # Total conversations owned by user
        # ---------------------------------------------

        conversations = await db.scalar(
            select(
                func.count(Conversation.id)
            ).where(
                Conversation.user_id == user_id
            )
        )


        # ---------------------------------------------
        # Documents uploaded by user
        # ---------------------------------------------

        documents = await db.scalar(
            select(
                func.count(Document.id)
            ).where(
                Document.uploaded_by == user_id
            )
        )


        # ---------------------------------------------
        # AI responses generated for user's chats
        # ---------------------------------------------

        ai_responses = await db.scalar(
            select(
                func.count(Message.id)
            )
            .join(
                Conversation,
                Message.conversation_id
                == Conversation.id,
            )
            .where(
                Conversation.user_id == user_id,
                Message.role == "assistant",
            )
        )


        # ---------------------------------------------
        # Average response time
        # ---------------------------------------------
        #
        # Not implemented yet because your Message model
        # does not currently store response duration.
        #

        average_response_time = 0.0


        return {
            "conversations": conversations or 0,
            "documents": documents or 0,
            "ai_responses": ai_responses or 0,
            "average_response_time": average_response_time,
        }