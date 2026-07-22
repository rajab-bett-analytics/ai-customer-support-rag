"""
Document repository.

Provides document-specific database operations.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.document import Document
from backend.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """
    Repository for document-specific database operations.
    """

    def __init__(self) -> None:
        super().__init__(Document)

    async def get_by_id(
        self,
        db: AsyncSession,
        document_id: int,
    ) -> Document | None:
        """
        Retrieve a document by its ID.
        """
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filename(
        self,
        db: AsyncSession,
        filename: str,
    ) -> Document | None:
        """
        Retrieve a document by its original filename.
        """
        result = await db.execute(
            select(Document).where(Document.filename == filename)
        )
        return result.scalar_one_or_none()

    async def get_by_stored_filename(
        self,
        db: AsyncSession,
        stored_filename: str,
    ) -> Document | None:
        """
        Retrieve a document by its stored filename.
        """
        result = await db.execute(
            select(Document).where(
                Document.stored_filename == stored_filename
            )
        )
        return result.scalar_one_or_none()

    async def get_by_owner(
        self,
        db: AsyncSession,
        uploaded_by: int,
    ) -> list[Document]:
        """
        Retrieve all documents uploaded by a specific user.
        """
        result = await db.execute(
            select(Document).where(
                Document.uploaded_by == uploaded_by
            )
        )
        return list(result.scalars().all())

    async def get_by_status(
        self,
        db: AsyncSession,
        status: str,
    ) -> list[Document]:
        """
        Retrieve all documents with a given processing status.
        """
        result = await db.execute(
            select(Document).where(
                Document.status == status
            )
        )
        return list(result.scalars().all())