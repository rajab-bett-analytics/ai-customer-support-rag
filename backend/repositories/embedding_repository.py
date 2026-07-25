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
        threshold: float = 0.45,
    ) -> list[Embedding]:
        """
        Retrieve relevant document chunks using pgvector
        cosine similarity.

        Only returns chunks above the relevance threshold
        to prevent unrelated context being sent to the LLM.

        Args:
            db: Database session.
            query_embedding: User query vector.
            limit: Maximum results.
            threshold: Maximum cosine distance allowed.

        Returns:
            Relevant document chunks.
        """

        distance = Embedding.embedding.cosine_distance(
            query_embedding
        )

        result = await db.execute(
            select(Embedding)
            .where(
                distance < threshold
            )
            .order_by(distance)
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
        Retrieve document chunks using keyword matching.

        Removes common words to avoid noisy searches.
        """

        stop_words = {
            "how",
            "many",
            "what",
            "who",
            "where",
            "when",
            "why",
            "is",
            "are",
            "the",
            "a",
            "an",
            "of",
            "to",
            "for",
            "in",
            "on",
            "and",
        }

        keywords = [
            word.lower().strip()
            for word in query.split()
            if (
                word.lower().strip()
                and word.lower().strip()
                not in stop_words
            )
        ]

        if not keywords:
            return []

        conditions = [
            Embedding.chunk_text.ilike(
                f"%{keyword}%"
            )
            for keyword in keywords
        ]

        result = await db.execute(
            select(Embedding)
            .where(
                or_(*conditions)
            )
            .limit(limit)
        )

        return list(result.scalars().all())