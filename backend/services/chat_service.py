"""
Chat service.

Coordinates Retrieval-Augmented Generation (RAG) by
retrieving relevant document context, managing
conversations, and generating grounded responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.conversation import Conversation
from backend.services.conversation_service import ConversationService
from backend.services.retrieval_service import RetrievalService


class ChatService:
    """
    Handles question answering using Retrieval-Augmented
    Generation (RAG).
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

        self.retrieval_service = RetrievalService()
        self.conversation_service = ConversationService()

    async def ask(
        self,
        db: AsyncSession,
        user_id: int,
        question: str,
        conversation_id: int | None = None,
    ) -> tuple[int, str, list[dict]]:
        """
        Answer a user's question while persisting the
        conversation history.

        Returns:
            Conversation ID, AI answer, and retrieved
            document sources.
        """

        conversation = await self._get_or_create_conversation(
            db=db,
            user_id=user_id,
            conversation_id=conversation_id,
            question=question,
        )

        await self.conversation_service.save_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=question,
        )

        history = await self.conversation_service.get_history(
            db=db,
            conversation_id=conversation.id,
        )

        context, embeddings = (
            await self.retrieval_service.retrieve_context(
                db=db,
                query=question,
            )
        )

        if not context:

            answer = (
                "I couldn't find any relevant information "
                "in the uploaded documents."
            )

        else:

            prompt = self._build_prompt(
                history=history,
                question=question,
                context=context,
            )

            try:

                response = self.client.models.generate_content(
                    model=settings.CHAT_MODEL,
                    contents=prompt,
                )

                answer = response.text.strip()

            except Exception as exc:

                raise RuntimeError(
                    f"Failed to generate AI response: {exc}"
                ) from exc

        await self.conversation_service.save_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )

        sources = [
            {
                "document_id": embedding.document_id,
                "chunk_index": embedding.chunk_index,
            }
            for embedding in embeddings
        ]

        return (
            conversation.id,
            answer,
            sources,
        )

    async def _get_or_create_conversation(
        self,
        db: AsyncSession,
        user_id: int,
        conversation_id: int | None,
        question: str,
    ) -> Conversation:
        """
        Retrieve an existing conversation or create one.
        """

        if conversation_id is not None:

            conversation = (
                await self.conversation_service.get_conversation(
                    db=db,
                    conversation_id=conversation_id,
                )
            )

            if conversation is not None:
                return conversation

        return await self.conversation_service.create_conversation(
            db=db,
            user_id=user_id,
            title=question[:60],
        )

    def _build_prompt(
        self,
        history: str,
        question: str,
        context: str,
    ) -> str:
        """
        Construct the prompt sent to Gemini.
        """

        return f"""
You are an AI Customer Support Assistant.

Your job is to answer customer questions using ONLY the
provided document context and conversation history.

Rules:

- Do not use outside knowledge.
- Do not invent facts.
- Use the conversation history to understand follow-up
  questions.
- Base your answer only on the retrieved document context.
- If the answer cannot be found in the document context,
  respond exactly:

I don't have enough information in the uploaded documents.

Conversation History:
{history}

Document Context:
{context}

Current Question:
{question}

Answer:
"""