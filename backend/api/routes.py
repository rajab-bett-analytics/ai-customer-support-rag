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

from backend.api.auth import router as auth_router

# ---------------------------------------------------------
# Main API Router
# ---------------------------------------------------------

api_router = APIRouter()

# ---------------------------------------------------------
# Register feature routers
# ---------------------------------------------------------

api_router.include_router(auth_router)