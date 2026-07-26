"""
Chat API.

Provides endpoints for interacting with the AI Customer
Support Assistant using Retrieval-Augmented Generation
(RAG).

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from backend.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a Question",
    description=(
        "Submit a question to the AI Customer Support "
        "Assistant. The service automatically determines "
        "whether the request requires document retrieval "
        "or a general conversational response."
    ),
)
async def ask_question(
    request: ChatRequest,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> ChatResponse:
    """
    Process a user's question and return an AI-generated
    response together with any retrieved document sources.
    """

    conversation_id, answer, sources = (
        await chat_service.ask(
            db=db,
            user_id=current_user.id,
            question=request.question,
            conversation_id=request.conversation_id,
        )
    )

    return ChatResponse(
        conversation_id=conversation_id,
        question=request.question,
        answer=answer,
        sources=sources,
    )