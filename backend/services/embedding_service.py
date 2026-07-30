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
        Generate embedding vector.

        Uses the configured embedding model.
        """

        if not text.strip():

            raise EmbeddingError(
                "Cannot generate embedding for empty text."
            )


        logger.info(
            "Generating embedding."
        )


        try:

            response = (
                self.client.models.embed_content(
                    model=settings.EMBEDDING_MODEL,
                    contents=text,
                )
            )


            if (
                not response.embeddings
                or not response.embeddings[0].values
            ):

                raise EmbeddingError(
                    "Embedding response was empty."
                )


            return (
                response.embeddings[0].values
            )


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
        Generate embedding for search query.
        """

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
        Generate and store one embedding.
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
                "Failed storing embedding."
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
        Generate embeddings for document chunks.
        """


        embeddings: list[Embedding] = []


        try:

            for chunk in chunks:


                chunk_text = str(
                    chunk["text"]
                )


                vector = (
                    await self.generate_embedding(
                        chunk_text,
                    )
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
                "%s embeddings created.",
                len(results),
            )


            return results



        except Exception as exc:


            logger.exception(
                "Failed creating embeddings."
            )


            raise EmbeddingError(
                "Unable to create embeddings."
            ) from exc



    async def search_similar_chunks(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
        threshold: float = 0.45,
        embedding_model: str | None = None,
    ) -> list[Embedding]:
        """
        Search similar document chunks.
        """

        query_embedding = await self.create_query_embedding(
            query,
        )

        try:

            results = (
                await self.embedding_repository.similarity_search(
                    db=db,
                    query_embedding=query_embedding,
                    limit=limit,
                    threshold=threshold,
                    embedding_model=embedding_model,
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

            print("\n" + "=" * 80)
            print("ORIGINAL EXCEPTION")
            print("=" * 80)
            print(f"Type: {type(exc).__name__}")
            print(f"Message: {exc}")
            print("=" * 80 + "\n")

            raise