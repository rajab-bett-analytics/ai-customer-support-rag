from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import api_router
from backend.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-ready AI Customer Support platform "
        "powered by Retrieval-Augmented Generation (RAG)."
    ),
    version=settings.APP_VERSION,
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Serve uploaded PDFs
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOADS_DIRECTORY = (
    PROJECT_ROOT
    / "storage"
    / "uploads"
)

UPLOADS_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIRECTORY),
    name="uploads",
)

# ---------------------------------------------------------
# API
# ---------------------------------------------------------

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "AI Customer Support RAG API is running."
    }