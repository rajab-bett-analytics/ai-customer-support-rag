"""
Conversation API.

Provides endpoints for managing user conversations.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.conversation import (
    ConversationResponse,
    ConversationSummary,
    MessageResponse,
)
from backend.services.conversation_service import (
    ConversationService,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

conversation_service = ConversationService()


@router.get(
    "",
    response_model=list[ConversationSummary],
    summary="List conversations",
)
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ConversationSummary]:
    """
    Retrieve all conversations belonging to the
    authenticated user.
    """

    conversations = await conversation_service.get_user_conversations(
        db=db,
        user_id=current_user.id,
    )

    return conversations


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get conversation",
)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationResponse:
    """
    Retrieve a conversation and all its messages.
    """

    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    messages = await conversation_service.get_messages(
        db=db,
        conversation_id=conversation.id,
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        messages=[
            MessageResponse.model_validate(message)
            for message in messages
        ],
    )


@router.delete(
    "/{conversation_id}",
    summary="Delete conversation",
)
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Delete a conversation.
    """

    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    await conversation_service.delete_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    return {
        "message": "Conversation deleted successfully."
    }