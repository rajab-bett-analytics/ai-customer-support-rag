"""
Chat API.

Provides an endpoint for asking questions against the
document knowledge base using Retrieval-Augmented Generation
(RAG).

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import APIRouter, Depends
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


@router.post(
    "",
    response_model=ChatResponse,
    summary="Ask a question",
)
async def ask_question(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """
    Ask a question against the uploaded knowledge base.
    """

    conversation_id, answer, sources = await chat_service.ask(
        db=db,
        user_id=current_user.id,
        question=request.question,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        question=request.question,
        answer=answer,
        sources=sources,
    )