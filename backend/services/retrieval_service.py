"""
Retrieval service.

Retrieves the most relevant document chunks for a user's
question using hybrid retrieval.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.embedding import Embedding
from backend.repositories.embedding_repository import (
    EmbeddingRepository,
)
from backend.services.embedding_service import (
    EmbeddingService,
)


class RetrievalService:
    """
    Handles Retrieval-Augmented Generation (RAG)
    retrieval using both vector similarity and
    keyword search.
    """

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.embedding_repository = EmbeddingRepository()

    async def retrieve_context(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> tuple[str, list[Embedding]]:
        """
        Retrieve relevant document context using hybrid
        retrieval.

        Args:
            db: Database session.
            query: User question.
            limit: Maximum number of chunks from each
                retrieval strategy.

        Returns:
            A tuple containing:

            - Combined context string.
            - Retrieved embedding objects.
        """

        vector_results = (
            await self.embedding_service.search_similar_chunks(
                db=db,
                query=query,
                limit=limit,
            )
        )

        keyword_results = (
            await self.embedding_repository.keyword_search(
                db=db,
                query=query,
                limit=limit,
            )
        )

        combined: list[Embedding] = []
        seen_ids: set[int] = set()

        for embedding in vector_results + keyword_results:

            if embedding.id in seen_ids:
                continue

            seen_ids.add(embedding.id)
            combined.append(embedding)

        if not combined:
            return "", []

        context = "\n\n".join(
            embedding.chunk_text
            for embedding in combined
        )

        return context, combined