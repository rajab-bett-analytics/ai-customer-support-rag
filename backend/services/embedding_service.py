"""
Embedding service.

Generates vector embeddings for document chunks and user
queries, then stores document embeddings in PostgreSQL.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.exceptions import EmbeddingError
from backend.core.logger import get_logger
from backend.models.embedding import Embedding
from backend.repositories.embedding_repository import (
    EmbeddingRepository,
)


logger = get_logger(__name__)


class EmbeddingService:
    """
    Handles embedding generation and persistence.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

        self.embedding_repository = (
            EmbeddingRepository()
        )

    async def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding vector for any text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """

        logger.info(
            "Generating embedding."
        )

        try:

            response = self.client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
            )

            return response.embeddings[0].values

        except Exception as exc:

            logger.exception(
                "Failed to generate embedding."
            )

            raise EmbeddingError(
                "Unable to generate embedding."
            ) from exc

    async def create_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user's search query.

        Args:
            query: User question.

        Returns:
            Query embedding vector.
        """

        logger.info(
            "Generating query embedding."
        )

        return await self.generate_embedding(
            query,
        )

    async def create_embedding(
        self,
        db: AsyncSession,
        document_id: int,
        page_number: int,
        chunk_index: int,
        chunk_text: str,
        section: str | None = None,
    ) -> Embedding:
        """
        Generate and store a single document embedding.
        """

        vector = await self.generate_embedding(
            chunk_text,
        )

        embedding = Embedding(
            document_id=document_id,
            page_number=page_number,
            chunk_index=chunk_index,
            section=section,
            chunk_text=chunk_text,
            embedding=vector,
        )

        try:

            result = (
                await self.embedding_repository.create(
                    db=db,
                    embedding=embedding,
                )
            )

            logger.info(
                "Embedding stored successfully."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Failed to store embedding."
            )

            raise EmbeddingError(
                "Unable to store embedding."
            ) from exc

    async def create_embeddings(
        self,
        db: AsyncSession,
        document_id: int,
        chunks: list[dict[str, int | str]],
    ) -> list[Embedding]:
        """
        Generate embeddings for all document chunks and
        store them in a single database transaction.

        Args:
            db: Database session.
            document_id: Parent document ID.
            chunks: Structured document chunks.

        Returns:
            Persisted Embedding objects.
        """

        logger.info(
            "Generating embeddings for %s chunks.",
            len(chunks),
        )

        embeddings: list[Embedding] = []

        try:

            for chunk in chunks:

                chunk_text = str(
                    chunk["text"]
                )

                vector = await self.generate_embedding(
                    chunk_text,
                )

                embeddings.append(
                    Embedding(
                        document_id=document_id,
                        page_number=int(
                            chunk["page"]
                        ),
                        chunk_index=int(
                            chunk["chunk_index"]
                        ),
                        section=None,
                        chunk_text=chunk_text,
                        embedding=vector,
                    )
                )

            results = (
                await self.embedding_repository.create_many(
                    db=db,
                    embeddings=embeddings,
                )
            )

            logger.info(
                "%s embeddings stored successfully.",
                len(results),
            )

            return results

        except Exception as exc:

            logger.exception(
                "Failed to create document embeddings."
            )

            raise EmbeddingError(
                "Unable to create document embeddings."
            ) from exc

    async def search_similar_chunks(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> list[Embedding]:
        """
        Retrieve the most relevant document chunks for
        a user's query.

        Args:
            db: Database session.
            query: User question.
            limit: Maximum number of chunks to retrieve.

        Returns:
            Most similar document chunks.
        """

        logger.info(
            "Searching similar document chunks."
        )

        try:

            query_embedding = (
                await self.create_query_embedding(
                    query,
                )
            )

            results = (
                await self.embedding_repository.similarity_search(
                    db=db,
                    query_embedding=query_embedding,
                    limit=limit,
                )
            )

            logger.info(
                "Retrieved %s similar chunks.",
                len(results),
            )

            return results

        except Exception as exc:

            logger.exception(
                "Similarity search failed."
            )

            raise EmbeddingError(
                "Unable to search document embeddings."
            ) from exc