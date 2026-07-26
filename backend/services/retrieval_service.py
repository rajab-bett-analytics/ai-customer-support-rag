"""
Retrieval service.

Retrieves the most relevant document chunks for a user's
question using hybrid retrieval.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import RetrievalError
from backend.core.logger import get_logger
from backend.models.embedding import Embedding
from backend.repositories.embedding_repository import (
    EmbeddingRepository,
)
from backend.services.embedding_service import (
    EmbeddingService,
)


logger = get_logger(__name__)


class RetrievalService:
    """
    Handles Retrieval-Augmented Generation (RAG)
    retrieval using vector similarity together with
    keyword search.
    """

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.embedding_repository = (
            EmbeddingRepository()
        )

    async def retrieve_context(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> tuple[str, list[Embedding]]:
        """
        Retrieve the most relevant document chunks.

        Args:
            db: Database session.
            query: User question.
            limit: Maximum number of retrieved chunks.

        Returns:
            A formatted context string together with the
            retrieved embedding objects.
        """

        logger.info(
            "Retrieving context for query: %s",
            query,
        )

        try:

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

            for embedding in (
                vector_results + keyword_results
            ):

                if embedding.id in seen_ids:
                    continue

                seen_ids.add(
                    embedding.id
                )

                combined.append(
                    embedding
                )

            if not combined:

                logger.info(
                    "No relevant document chunks found."
                )

                return "", []

            context_parts: list[str] = []

            for embedding in combined:

                filename = (
                    embedding.document.filename
                    if embedding.document is not None
                    else "Unknown document"
                )

                page = getattr(
                    embedding,
                    "page_number",
                    None,
                )

                section = getattr(
                    embedding,
                    "section",
                    None,
                )

                metadata = [
                    f"Document: {filename}",
                    f"Chunk: {embedding.chunk_index}",
                ]

                if page is not None:
                    metadata.append(
                        f"Page: {page}"
                    )

                if section:
                    metadata.append(
                        f"Section: {section}"
                    )

                context_parts.append(
                    (
                        "\n".join(metadata)
                        + "\n\n"
                        + embedding.chunk_text
                    )
                )

            context = (
                "\n\n"
                "------------------------------"
                "\n\n"
            ).join(
                context_parts
            )

            logger.info(
                "Retrieved %s unique chunks.",
                len(combined),
            )

            return (
                context,
                combined,
            )

        except Exception as exc:

            logger.exception(
                "Document retrieval failed."
            )

            raise RetrievalError(
                "Unable to retrieve relevant document context."
            ) from exc