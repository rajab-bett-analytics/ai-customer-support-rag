"""
Document service.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.document import Document
from backend.models.user import User
from backend.repositories.document_repository import DocumentRepository


class DocumentService:
    """
    Handles document-related business logic.
    """

    ALLOWED_CONTENT_TYPES = {"application/pdf"}

    def __init__(self) -> None:
        self.document_repository = DocumentRepository()

    async def save_document(
        self,
        db: AsyncSession,
        current_user: User,
        file: UploadFile,
    ) -> Document:
        """
        Validate, store and persist an uploaded PDF.
        """

        self._validate_pdf(file)

        upload_dir = Path(settings.UPLOAD_DIRECTORY)
        upload_dir.mkdir(parents=True, exist_ok=True)

        stored_filename = f"{uuid4()}.pdf"
        file_path = upload_dir / stored_filename

        file_bytes = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)

        document = Document(
            uploaded_by=current_user.id,
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            mime_type=file.content_type,
            file_size=len(file_bytes),
            status="uploaded",
        )

        return await self.document_repository.create(
            db,
            document,
        )

    @classmethod
    def _validate_pdf(
        cls,
        file: UploadFile,
    ) -> None:
        """
        Validate uploaded document.
        """

        if file.content_type not in cls.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )