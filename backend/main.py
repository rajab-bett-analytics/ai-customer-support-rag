"""
Main application entry point.

This module creates and configures the FastAPI application.

As the project grows, additional routers, middleware,
event handlers, and services will be registered here.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import api_router
from backend.core.config import settings

# ---------------------------------------------------------
# Create the FastAPI application instance.
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-ready AI Customer Support platform "
        "powered by FastAPI and Retrieval-Augmented "
        "Generation (RAG)."
    ),
    version=settings.APP_VERSION,
)

# ---------------------------------------------------------
# Configure CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Register API routers
# ---------------------------------------------------------

app.include_router(api_router)

# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.
    """

    return {
        "message": "AI Customer Support RAG API is running."
    }