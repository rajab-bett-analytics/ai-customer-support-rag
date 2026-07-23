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
from backend.models.embedding import Embedding
from backend.repositories.embedding_repository import (
    EmbeddingRepository,
)


class EmbeddingService:
    """
    Handles embedding generation and persistence.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

        self.embedding_repository = EmbeddingRepository()

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

        response = self.client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text,
        )

        return response.embeddings[0].values

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

        return await self.generate_embedding(query)

    async def create_embedding(
        self,
        db: AsyncSession,
        document_id: int,
        chunk_index: int,
        chunk_text: str,
    ) -> Embedding:
        """
        Generate and store a single document embedding.
        """

        vector = await self.generate_embedding(
            chunk_text,
        )

        embedding = Embedding(
            document_id=document_id,
            chunk_index=chunk_index,
            chunk_text=chunk_text,
            embedding=vector,
        )

        return await self.embedding_repository.create(
            db,
            embedding,
        )

    async def create_embeddings(
        self,
        db: AsyncSession,
        document_id: int,
        chunks: list[str],
    ) -> list[Embedding]:
        """
        Generate embeddings for all document chunks and
        store them in a single database transaction.

        Args:
            db: Database session.
            document_id: Parent document ID.
            chunks: List of cleaned text chunks.

        Returns:
            Persisted Embedding objects.
        """

        embeddings: list[Embedding] = []

        for index, chunk in enumerate(chunks):

            vector = await self.generate_embedding(
                chunk,
            )

            embeddings.append(
                Embedding(
                    document_id=document_id,
                    chunk_index=index,
                    chunk_text=chunk,
                    embedding=vector,
                )
            )

        return await self.embedding_repository.create_many(
            db,
            embeddings,
        )

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

        query_embedding = await self.create_query_embedding(
            query,
        )

        return await self.embedding_repository.similarity_search(
            db=db,
            query_embedding=query_embedding,
            limit=limit,
        )