"""
Embedding repository.

Provides database operations for document embeddings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.embedding import Embedding
from backend.repositories.base import BaseRepository


class EmbeddingRepository(BaseRepository[Embedding]):
    """
    Repository for embedding-specific database operations.
    """

    def __init__(self) -> None:
        super().__init__(Embedding)

    async def get_by_document(
        self,
        db: AsyncSession,
        document_id: int,
    ) -> list[Embedding]:
        """
        Retrieve all embeddings belonging to a document.
        """

        result = await db.execute(
            select(Embedding).where(
                Embedding.document_id == document_id
            )
        )

        return list(result.scalars().all())

    async def create_many(
        self,
        db: AsyncSession,
        embeddings: list[Embedding],
    ) -> list[Embedding]:
        """
        Persist multiple embeddings in a single transaction.
        """

        db.add_all(embeddings)

        await db.commit()

        for embedding in embeddings:
            await db.refresh(embedding)

        return embeddings

    async def similarity_search(
        self,
        db: AsyncSession,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[Embedding]:
        """
        Retrieve the most similar document chunks using
        pgvector cosine distance.

        Results are ordered from most similar to least similar.
        """

        result = await db.execute(
            select(Embedding)
            .order_by(
                Embedding.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
        )

        return list(result.scalars().all())

    async def keyword_search(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> list[Embedding]:
        """
        Retrieve document chunks containing the query
        keywords using PostgreSQL ILIKE matching.
        """

        keywords = [
            word.strip()
            for word in query.split()
            if word.strip()
        ]

        if not keywords:
            return []

        conditions = [
            Embedding.chunk_text.ilike(f"%{word}%")
            for word in keywords
        ]

        result = await db.execute(
            select(Embedding)
            .where(or_(*conditions))
            .limit(limit)
        )

        return list(result.scalars().all())