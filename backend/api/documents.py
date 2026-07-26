"""
Document API.

Provides endpoints for uploading, listing, and deleting
knowledge base documents used by the Retrieval-Augmented
Generation (RAG) pipeline.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.services.document_service import (
    DocumentService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]

UploadedFile = Annotated[
    UploadFile,
    File(...),
]


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document",
    description=(
        "Upload a PDF document, extract its text, generate "
        "embeddings, and add it to the searchable knowledge "
        "base."
    ),
)
async def upload_document(
    file: UploadedFile,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> dict:
    """
    Upload and process a PDF document.
    """

    return await document_service.save_document(
        db=db,
        current_user=current_user,
        file=file,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List Documents",
    description=(
        "Retrieve all knowledge base documents uploaded "
        "by the authenticated user."
    ),
)
async def list_documents(
    current_user: CurrentUser,
    db: DatabaseSession,
) -> list:
    """
    Retrieve all uploaded documents.
    """

    return await document_service.get_documents(
        db=db,
        current_user=current_user,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Document",
    description=(
        "Delete a document together with all associated "
        "embeddings from the knowledge base."
    ),
)
async def delete_document(
    document_id: int,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> dict:
    """
    Delete a document owned by the authenticated user.
    """

    await document_service.delete_document(
        db=db,
        current_user=current_user,
        document_id=document_id,
    )

    return {
        "message": "Document deleted successfully."
    }