"""
Document repository.

Provides document-specific database operations.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.document import Document
from backend.repositories.base import BaseRepository


class DocumentRepository(
    BaseRepository[Document]
):
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
            select(Document)
            .options(
                selectinload(
                    Document.embeddings,
                )
            )
            .where(
                Document.id == document_id,
            )
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
            select(Document).where(
                Document.filename == filename,
            )
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
                Document.stored_filename
                == stored_filename,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_owner(
        self,
        db: AsyncSession,
        uploaded_by: int,
    ) -> list[Document]:
        """
        Retrieve all documents uploaded by a user.
        """

        result = await db.execute(
            select(Document)
            .where(
                Document.uploaded_by
                == uploaded_by,
            )
            .order_by(
                Document.created_at.desc(),
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_processed_documents(
        self,
        db: AsyncSession,
    ) -> list[Document]:
        """
        Retrieve all successfully processed documents.
        """

        result = await db.execute(
            select(Document)
            .where(
                Document.status == "processed",
            )
            .order_by(
                Document.created_at.desc(),
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_by_status(
        self,
        db: AsyncSession,
        status: str,
    ) -> list[Document]:
        """
        Retrieve documents by processing status.
        """

        result = await db.execute(
            select(Document)
            .where(
                Document.status == status,
            )
            .order_by(
                Document.created_at.desc(),
            )
        )

        return list(
            result.scalars().all()
        )

    async def count_documents(
        self,
        db: AsyncSession,
    ) -> int:
        """
        Count all documents.
        """

        result = await db.execute(
            select(
                func.count(Document.id)
            )
        )

        return int(
            result.scalar_one()
        )

    async def exists(
        self,
        db: AsyncSession,
        document_id: int,
    ) -> bool:
        """
        Check whether a document exists.
        """

        result = await db.execute(
            select(Document.id).where(
                Document.id == document_id,
            )
        )

        return result.scalar_one_or_none() is not None

    async def delete_document(
        self,
        db: AsyncSession,
        document: Document,
    ) -> None:
        """
        Delete a document.
        """

        await db.delete(document)
        await db.commit()