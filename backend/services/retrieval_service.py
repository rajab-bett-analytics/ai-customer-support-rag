"""
Retrieval service.

Retrieves the most relevant document chunks for a user's
question using hybrid retrieval.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from sqlalchemy.ext.asyncio import AsyncSession

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
    Handles Retrieval-Augmented Generation (RAG).

    Uses:

    - Vector semantic search
    - Keyword search
    - Result merging
    - Metadata preservation
    """

    def __init__(self) -> None:

        self.embedding_service = (
            EmbeddingService()
        )

        self.embedding_repository = (
            EmbeddingRepository()
        )

    async def retrieve_context(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
        similarity_threshold: float = 0.75,
        embedding_model: str | None = None,
    ) -> tuple[str, list[Embedding]]:
        """
        Retrieve relevant document chunks.
        """

        logger.info(
            "Retrieving context | query=%s | limit=%s | threshold=%s",
            query,
            limit,
            similarity_threshold,
        )

        try:

            logger.info("Starting vector search...")

            vector_results = (
                await self.embedding_service.search_similar_chunks(
                    db=db,
                    query=query,
                    limit=limit,
                    threshold=similarity_threshold,
                    embedding_model=embedding_model,
                )
            )

            logger.info(
                "Vector search returned %s results.",
                len(vector_results),
            )

            logger.info("Starting keyword search...")

            keyword_results = (
                await self.embedding_repository.keyword_search(
                    db=db,
                    query=query,
                    limit=limit,
                )
            )

            logger.info(
                "Keyword search returned %s results.",
                len(keyword_results),
            )

            combined: list[Embedding] = []

            seen: set[int] = set()

            for embedding in (
                vector_results
                + keyword_results
            ):

                if embedding.id in seen:
                    continue

                seen.add(
                    embedding.id
                )

                combined.append(
                    embedding
                )

            if not combined:

                logger.info(
                    "No matching document chunks found."
                )

                return "", []

            context_blocks: list[str] = []

            for index, embedding in enumerate(
                combined,
                start=1,
            ):

                document_name = (
                    embedding.document.filename
                    if embedding.document
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

                similarity = getattr(
                    embedding,
                    "similarity_score",
                    None,
                )

                block = [
                    "=" * 60,
                    f"SOURCE {index}",
                    "",
                    f"Document : {document_name}",
                    f"Chunk    : {embedding.chunk_index}",
                ]

                if page is not None:
                    block.append(
                        f"Page     : {page}"
                    )

                if section:
                    block.append(
                        f"Section  : {section}"
                    )

                if similarity is not None:
                    block.append(
                        f"Score    : {similarity:.3f}"
                    )

                block.extend(
                    [
                        "",
                        "Content:",
                        embedding.chunk_text.strip(),
                        "=" * 60,
                    ]
                )

                context_blocks.append(
                    "\n".join(block)
                )

            context = "\n\n".join(
                context_blocks
            )

            logger.info(
                "Retrieved %s unique chunks.",
                len(combined),
            )

            return (
                context,
                combined,
            )

        except Exception:

            logger.exception(
                "Document retrieval failed."
            )

            # Re-raise the ORIGINAL exception so the full traceback
            # shows the exact failing line.
            raise