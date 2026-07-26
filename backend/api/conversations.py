"""
Conversation API.

Provides endpoints for retrieving and managing user
conversations.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
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

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


@router.get(
    "",
    response_model=list[ConversationSummary],
    status_code=status.HTTP_200_OK,
    summary="List Conversations",
    description=(
        "Retrieve all conversations belonging to the "
        "authenticated user."
    ),
)
async def list_conversations(
    db: DatabaseSession,
    current_user: CurrentUser,
) -> list[ConversationSummary]:
    """
    Retrieve all conversations for the current user.
    """

    return await conversation_service.get_user_conversations(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Conversation",
    description=(
        "Retrieve a conversation together with all "
        "messages exchanged within it."
    ),
)
async def get_conversation(
    conversation_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> ConversationResponse:
    """
    Retrieve a single conversation.
    """

    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if (
        conversation is None
        or conversation.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    status_code=status.HTTP_200_OK,
    summary="Delete Conversation",
    description=(
        "Delete one of the authenticated user's "
        "conversations."
    ),
)
async def delete_conversation(
    conversation_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> dict[str, str]:
    """
    Delete a conversation.
    """

    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if (
        conversation is None
        or conversation.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    await conversation_service.delete_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    return {
        "message": (
            "Conversation deleted successfully."
        )
    }