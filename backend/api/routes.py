"""
Application API router.

This module aggregates all API routers into a single
router that is registered by the FastAPI application.

As new features are added, their routers should be
included here.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import APIRouter
from backend.api.conversations import (
    router as conversation_router,
)

from backend.api.auth import router as auth_router
from backend.api.documents import router as document_router
from backend.api.chat import router as chat_router

# ---------------------------------------------------------
# Main API Router
# ---------------------------------------------------------

api_router = APIRouter()

# ---------------------------------------------------------
# Register feature routers
# ---------------------------------------------------------

api_router.include_router(auth_router)
api_router.include_router(document_router)
api_router.include_router(chat_router)
api_router.include_router(conversation_router)