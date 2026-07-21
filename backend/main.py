"""
Main application entry point.

This module creates and configures the FastAPI application.

As the project grows, additional routers, middleware,
event handlers, and services will be registered here.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import FastAPI
from backend.core.config import settings

# ---------------------------------------------------------
# Create the FastAPI application instance.
#
# This object is the heart of the application.
# Uvicorn imports this object when starting the server.
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready AI Customer Support platform powered by FastAPI and Retrieval-Augmented Generation (RAG).",
    version=settings.APP_NAME,
)

# ---------------------------------------------------------
# Root endpoint
#
# This endpoint is primarily used to verify that the API
# is running successfully.
# ---------------------------------------------------------


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        A simple JSON response confirming that
        the API is running.
    """
    return {
        "message": "AI Customer Support RAG API is running."
    }