from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.document import Document
from backend.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """
    Repository for Document-specific database operations.
    """

    def __init__(self):
        super().__init__(Document)

    async def get_by_filename(
        self,
        db: AsyncSession,
        filename: str,
    ) -> Document | None:
        result = await db.execute(
            select(Document).where(Document.filename == filename)
        )
        return result.scalar_one_or_none()

    async def get_by_owner(
        self,
        db: AsyncSession,
        owner_id: int,
    ) -> list[Document]:
        result = await db.execute(
            select(Document).where(Document.owner_id == owner_id)
        )
        return list(result.scalars().all())