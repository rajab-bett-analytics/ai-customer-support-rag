from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and process a PDF document.
    """

    return await document_service.save_document(
        db=db,
        current_user=current_user,
        file=file,
    )


@router.get("")
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all documents uploaded by the current user.
    """

    return await document_service.get_documents(
        db=db,
        current_user=current_user,
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a document owned by the current user.
    """

    await document_service.delete_document(
        db=db,
        current_user=current_user,
        document_id=document_id,
    )

    return {
        "message": "Document deleted successfully."
    }