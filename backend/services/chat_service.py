"""
Chat service.

Coordinates Retrieval-Augmented Generation (RAG) by
classifying user intent, retrieving relevant document
context, managing conversations, and generating AI
responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.enums.intent import Intent
from backend.models.conversation import Conversation
from backend.services.conversation_service import (
    ConversationService,
)
from backend.services.generation_service import (
    GenerationService,
)
from backend.services.intent_service import (
    IntentService,
)
from backend.services.retrieval_service import (
    RetrievalService,
)


class ChatService:
    """
    Coordinates AI conversations by routing requests
    to either conversational AI or the RAG pipeline.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

        self.intent_service = IntentService()
        self.generation_service = (
            GenerationService()
        )
        self.retrieval_service = (
            RetrievalService()
        )
        self.conversation_service = (
            ConversationService()
        )

    async def ask(
        self,
        db: AsyncSession,
        user_id: int,
        question: str,
        conversation_id: int | None = None,
    ) -> tuple[int, str, list[dict]]:
        """
        Process a user's question.

        Depending on the detected intent,
        route the request to either:

        - GenerationService
        - RetrievalService (RAG)

        Returns:
            Conversation ID,
            AI response,
            Retrieved sources.
        """

        conversation = (
            await self._get_or_create_conversation(
                db=db,
                user_id=user_id,
                conversation_id=conversation_id,
                question=question,
            )
        )

        await self.conversation_service.save_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=question,
        )

        history = (
            await self.conversation_service.get_history(
                db=db,
                conversation_id=conversation.id,
            )
        )

        intent = await self.intent_service.classify(
            question
        )

        embeddings = []

        if (
            intent.intent
            != Intent.DOCUMENT_QUERY
        ):

            answer = (
                await self.generation_service.generate(
                    history=history,
                    question=question,
                )
            )

            if (
                answer.strip()
                == "DOCUMENT_QUERY"
            ):

                intent.intent = (
                    Intent.DOCUMENT_QUERY
                )

        if (
            intent.intent
            == Intent.DOCUMENT_QUERY
        ):

            context, embeddings = (
                await self.retrieval_service.retrieve_context(
                    db=db,
                    query=question,
                )
            )

            if not context:

                answer = (
                    "I couldn't find that "
                    "information in the uploaded "
                    "documents. Please try asking "
                    "a question related to the "
                    "available documents."
                )

            else:

                prompt = self._build_prompt(
                    history=history,
                    question=question,
                    context=context,
                )

                try:

                    response = (
                        self.client.models.generate_content(
                            model=settings.CHAT_MODEL,
                            contents=prompt,
                        )
                    )

                    answer = (
                        response.text.strip()
                    )

                except Exception as exc:

                    raise RuntimeError(
                        "Failed to generate "
                        f"AI response: {exc}"
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


    def _build_prompt(
        self,
        history: str,
        question: str,
        context: str,
    ) -> str:
        """
        Build the Retrieval-Augmented Generation (RAG)
        prompt sent to Gemini.
        """

        return f"""
You are an AI Customer Support Assistant.

Your responsibility is to answer questions using ONLY
the provided document context.

Rules:

1. Answer ONLY using the supplied document context.

2. Never invent facts, policies, salaries, dates,
regulations, benefits, or procedures.

3. Use the conversation history to understand
follow-up questions.

4. If the answer is not explicitly stated in the
document context, reply exactly:

I couldn't find that information in the uploaded documents.

5. Format your answers professionally:

- Use Markdown.
- Use headings where appropriate.
- Use bullet points for lists.
- Use numbered lists for procedures.
- Use **bold** for important terms.
- Quote important values exactly as they appear.
- Keep answers clear and concise.

Conversation History:
{history}

Document Context:
{context}

Current Question:
{question}

Answer:
"""

    async def _get_or_create_conversation(
        self,
        db: AsyncSession,
        user_id: int,
        conversation_id: int | None,
        question: str,
    ) -> Conversation:
        """
        Retrieve an existing conversation or create
        a new one.
        """

        if conversation_id is not None:

            conversation = (
                await self.conversation_service
                .get_conversation(
                    db=db,
                    conversation_id=conversation_id,
                )
            )

            if conversation is not None:
                return conversation

        return (
            await self.conversation_service
            .create_conversation(
                db=db,
                user_id=user_id,
                title=question[:60],
            )
        )