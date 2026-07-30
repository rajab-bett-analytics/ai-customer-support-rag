"""
Chat service.

Coordinates Retrieval-Augmented Generation (RAG) by
classifying user intent, retrieving relevant document
context, managing conversations, and generating AI
responses.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from urllib.parse import quote

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.enums.intent import Intent
from backend.models.conversation import Conversation
from backend.models.user import User
from backend.repositories.user_repository import (
    UserRepository,
)
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
from backend.services.settings_service import (
    SettingsService,
)


class ChatResult(BaseModel):
    """
    Internal response returned by ChatService.
    """

    conversation_id: int
    answer: str
    sources: list[dict[str, object]]


class ChatService:
    """
    Coordinates AI conversations.

    Routes requests to:

    - General AI conversation
    - Retrieval-Augmented Generation pipeline
    """

    def __init__(self) -> None:

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

        self.settings_service = (
            SettingsService()
        )

        self.user_repository = (
            UserRepository()
        )


    async def ask(
        self,
        db: AsyncSession,
        user_id: int,
        question: str,
        conversation_id: int | None = None,
    ) -> ChatResult:
        """
        Process user question.
        """

        user = await self.user_repository.get_by_id(
            db,
            user_id,
        )


        if user is None:
            raise RuntimeError(
                "User not found."
            )


        user_settings = (
            await self.settings_service.get_settings(
                db=db,
                user=user,
            )
        )


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

        answer = ""


        # ==========================================
        # GENERAL CONVERSATION
        # ==========================================

        if intent.intent != Intent.DOCUMENT_QUERY:


            answer = (
                await self.generation_service.generate(
                    history=history,
                    question=question,
                    user_settings=user_settings,
                )
            )


            if answer.strip() == "DOCUMENT_QUERY":

                intent.intent = (
                    Intent.DOCUMENT_QUERY
                )


        # ==========================================
        # RAG PIPELINE
        # ==========================================

        if intent.intent == Intent.DOCUMENT_QUERY:


            context, embeddings = (
                await self.retrieval_service.retrieve_context(
                    db=db,
                    query=question,
                    limit=user_settings.top_k,
                )
            )


            if not context:

                answer = (
                    "I couldn't find that information "
                    "in the uploaded documents."
                )


            else:

                prompt = self._build_prompt(
                    history=history,
                    question=question,
                    context=context,
                    system_prompt=(
                        user_settings.system_prompt
                    ),
                )


                answer = (
                    await self.generation_service.generate_rag(
                        prompt=prompt,
                        user_settings=user_settings,
                    )
                )


        await self.conversation_service.save_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )


        sources = self._build_sources(
            embeddings
        )


        return ChatResult(
            conversation_id=conversation.id,
            answer=answer,
            sources=sources,
        )


    def _build_sources(
        self,
        embeddings,
    ) -> list[dict[str, object]]:
        """
        Build document citations.
        """

        seen = set()

        sources = []


        for embedding in embeddings:

            document = embedding.document


            if document is None:
                continue


            page = getattr(
                embedding,
                "page_number",
                None,
            )


            key = (
                embedding.document_id,
                page,
            )


            if key in seen:
                continue


            seen.add(key)


            sources.append(
                {
                    "document_id": (
                        embedding.document_id
                    ),

                    "document_name": (
                        document.filename
                    ),

                    "document_url": (
                        "http://localhost:8000/uploads/"
                        f"{quote(document.stored_filename)}"
                    ),

                    "page": page,

                    "chunk_index": (
                        embedding.chunk_index
                    ),

                    "section": (
                        embedding.section
                    ),

                    "chunk_text": (
                        embedding.chunk_text
                    ),
                }
            )


        return sources



    def _build_prompt(
        self,
        history: str,
        question: str,
        context: str,
        system_prompt: str | None,
    ) -> str:
        """
        Build RAG prompt.
        """

        return f"""
{system_prompt or "You are an AI Customer Support Assistant."}


RULES:

- Use ONLY supplied document context.
- Never invent information.
- Never create fake policies.
- If information is missing say:

I couldn't find that information in the uploaded documents.

- Include citations:

(Source: Document Name, Page X)

- Never mention chunks.


CONVERSATION HISTORY:

{history}


DOCUMENT CONTEXT:

{context}


QUESTION:

{question}


ANSWER:
"""


    async def _get_or_create_conversation(
        self,
        db: AsyncSession,
        user_id: int,
        conversation_id: int | None,
        question: str,
    ) -> Conversation:
        """
        Retrieve existing conversation or create one.
        """

        if conversation_id is not None:

            conversation = (
                await self.conversation_service.get_conversation(
                    db=db,
                    conversation_id=conversation_id,
                )
            )

            if conversation:
                return conversation


        return (
            await self.conversation_service.create_conversation(
                db=db,
                user_id=user_id,
                title=question[:60],
            )
        )