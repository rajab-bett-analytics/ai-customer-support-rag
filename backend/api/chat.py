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
        "Assistant. The assistant automatically decides "
        "whether Retrieval-Augmented Generation (RAG) "
        "is required, retrieves relevant document "
        "context when necessary, generates an answer, "
        "and returns supporting citations."
    ),
    response_description=(
        "AI-generated answer together with conversation "
        "information and document citations."
    ),
)
async def ask_question(
    request: ChatRequest,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> ChatResponse:
    """
    Ask the AI assistant a question.

    Workflow
    --------
    1. Validate the authenticated user.
    2. Retrieve relevant knowledge-base documents (if needed).
    3. Generate an AI response.
    4. Save the conversation.
    5. Return the answer together with supporting citations.
    """

    response = await chat_service.ask(
        db=db,
        user_id=current_user.id,
        question=request.question,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=response.conversation_id,
        question=request.question,
        answer=response.answer,
        sources=response.sources,
    )