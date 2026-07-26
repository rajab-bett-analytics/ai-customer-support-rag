"""
Embedding repository.

Provides database operations for document embeddings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.embedding import Embedding
from backend.repositories.base import BaseRepository


class EmbeddingRepository(
    BaseRepository[Embedding]
):
    """
    Repository for embedding-related database operations.
    """

    STOP_WORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "do",
        "does",
        "for",
        "from",
        "how",
        "in",
        "is",
        "it",
        "many",
        "of",
        "on",
        "or",
        "the",
        "to",
        "was",
        "were",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
    }

    def __init__(self) -> None:
        super().__init__(Embedding)

    async def get_by_document(
        self,
        db: AsyncSession,
        document_id: int,
    ) -> list[Embedding]:
        """
        Retrieve all embeddings for a document.
        """

        result = await db.execute(
            select(Embedding)
            .where(
                Embedding.document_id == document_id
            )
            .order_by(
                Embedding.page_number,
                Embedding.chunk_index,
            )
        )

        return list(result.scalars().all())

    async def create_many(
        self,
        db: AsyncSession,
        embeddings: list[Embedding],
    ) -> list[Embedding]:
        """
        Persist multiple embeddings.
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
        Retrieve semantically similar chunks.
        """

        distance = (
            Embedding.embedding.cosine_distance(
                query_embedding,
            )
        )

        result = await db.execute(
            select(Embedding)
            .options(
                selectinload(
                    Embedding.document,
                )
            )
            .where(
                distance < threshold,
            )
            .order_by(distance.asc())
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
        Retrieve chunks using keyword matching.
        """

        keywords = [
            word.lower().strip(".,?!")
            for word in query.split()
            if (
                word.lower().strip(".,?!")
                and word.lower().strip(".,?!")
                not in self.STOP_WORDS
            )
        ]

        if not keywords:
            return []

        conditions = [
            func.lower(
                Embedding.chunk_text
            ).contains(keyword)
            for keyword in keywords
        ]

        result = await db.execute(
            select(Embedding)
            .options(
                selectinload(
                    Embedding.document,
                )
            )
            .where(
                or_(*conditions)
            )
            .order_by(
                Embedding.page_number,
                Embedding.chunk_index,
            )
            .limit(limit)
        )

        return list(result.scalars().all())