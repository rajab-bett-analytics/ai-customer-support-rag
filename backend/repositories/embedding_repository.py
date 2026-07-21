from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.embedding import Embedding
from backend.repositories.base import BaseRepository


class EmbeddingRepository(BaseRepository[Embedding]):
    """
    Repository for Embedding-specific database operations.
    """

    def __init__(self):
        super().__init__(Embedding)

    async def get_by_document(
        self,
        db: AsyncSession,
        document_id: int,
    ) -> list[Embedding]:
        result = await db.execute(
            select(Embedding).where(
                Embedding.document_id == document_id
            )
        )
        return list(result.scalars().all())