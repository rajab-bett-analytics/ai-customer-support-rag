"""
Document service.

Handles document upload, validation, storage,
PDF text extraction, cleaning, chunking and
embedding generation.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.document import Document
from backend.models.user import User
from backend.repositories.document_repository import (
    DocumentRepository,
)
from backend.services.embedding_service import (
    EmbeddingService,
)
from backend.utils.chunker import chunk_text
from backend.utils.pdf import extract_text_from_pdf
from backend.utils.text import clean_text


class DocumentService:
    """
    Handles document-related business logic.
    """

    ALLOWED_CONTENT_TYPES = {
        "application/pdf"
    }

    def __init__(self) -> None:
        self.document_repository = (
            DocumentRepository()
        )

        self.embedding_service = (
            EmbeddingService()
        )

    async def save_document(
        self,
        db: AsyncSession,
        current_user: User,
        file: UploadFile,
    ) -> dict:
        """
        Upload, process and index a PDF document.
        """

        self._validate_pdf(file)

        upload_dir = Path(
            settings.UPLOAD_DIRECTORY
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        stored_filename = (
            f"{uuid4()}.pdf"
        )

        file_path = (
            upload_dir / stored_filename
        )

        file_bytes = await file.read()

        with open(
            file_path,
            "wb",
        ) as buffer:
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

        document = await self.document_repository.create(
            db,
            document,
        )

        try:

            pages = extract_text_from_pdf(
                file_path,
            )

            cleaned_pages: list[
                dict[str, int | str]
            ] = []

            for page in pages:
                cleaned_pages.append(
                    {
                        "page": page["page"],
                        "text": clean_text(
                            str(page["text"])
                        ),
                    }
                )

            chunks = chunk_text(
                cleaned_pages,
            )

            embeddings = (
                await self.embedding_service.create_embeddings(
                    db=db,
                    document_id=document.id,
                    chunks=chunks,
                )
            )

            # ---------------------------------------------
            # Processing metadata
            # ---------------------------------------------

            document.page_count = len(
                pages
            )

            document.chunk_count = len(
                chunks
            )

            document.embedding_count = len(
                embeddings
            )

            document.indexed_at = (
                datetime.utcnow()
            )

            document.error_message = None

            document.status = (
                "processed"
            )

            await db.commit()
            await db.refresh(document)

        except Exception as exc:

            document.status = (
                "failed"
            )

            document.error_message = (
                str(exc)
            )

            await db.commit()
            await db.refresh(document)

            raise HTTPException(
                status_code=500,
                detail=(
                    "Document processing "
                    f"failed: {exc}"
                ),
            ) from exc

        return {
            "document_id": document.id,
            "filename": document.filename,
            "status": document.status,
            "pages": document.page_count,
            "chunks_created": document.chunk_count,
            "embeddings_created": document.embedding_count,
            "file_size": document.file_size,
        }

    async def get_documents(
        self,
        db: AsyncSession,
        current_user: User,
    ) -> list[Document]:
        """
        Retrieve all documents uploaded by the current
        user.
        """

        return (
            await self.document_repository.get_by_owner(
                db=db,
                uploaded_by=current_user.id,
            )
        )

    async def delete_document(
        self,
        db: AsyncSession,
        current_user: User,
        document_id: int,
    ) -> None:
        """
        Delete a document owned by the current user.
        """

        document = (
            await self.document_repository.get_by_id(
                db=db,
                document_id=document_id,
            )
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        if document.uploaded_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Not authorized to "
                    "delete this document."
                ),
            )

        file_path = Path(
            document.file_path
        )

        if file_path.exists():
            file_path.unlink()

        await self.document_repository.delete_document(
            db=db,
            document=document,
        )

    @classmethod
    def _validate_pdf(
        cls,
        file: UploadFile,
    ) -> None:
        """
        Validate uploaded document.
        """

        if (
            file.content_type
            not in cls.ALLOWED_CONTENT_TYPES
        ):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )