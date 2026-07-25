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


        # Handle normal conversation first
        small_talk_answer = self._handle_small_talk(
            question
        )

        if small_talk_answer:

            answer = small_talk_answer
            embeddings = []

        else:

            context, embeddings = (
                await self.retrieval_service.retrieve_context(
                    db=db,
                    query=question,
                )
            )

            if not context:

                answer = (
                    "I couldn't find that information in "
                    "the uploaded documents. "
                    "Please try asking a question related "
                    "to the available documents."
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


    def _handle_small_talk(
        self,
        question: str,
    ) -> str | None:
        """
        Handle simple conversation without RAG.
        """

        message = question.lower().strip()


        greetings = {
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
        }


        if message in greetings:

            return (
                "Hello 👋\n\n"
                "I am your AI Customer Support Assistant. "
                "I can help answer questions from uploaded "
                "company documents and policies."
            )


        if (
            "who are you" in message
            or "what are you" in message
        ):

            return (
                "I am an AI Customer Support Assistant "
                "powered by Retrieval-Augmented Generation "
                "(RAG). I help users find accurate answers "
                "from uploaded company documents."
            )


        if message in {
            "thanks",
            "thank you",
            "thankyou",
        }:

            return (
                "You're welcome! 😊 "
                "Feel free to ask if you need anything else."
            )


        return None



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

You answer questions using the provided document
context.

Important rules:

1. Use ONLY the provided document context for factual
answers.

2. Never invent policies, numbers, dates, salaries,
or regulations.

3. If the answer is not available in the context,
say:
"I couldn't find that information in the uploaded
documents."

4. If the user asks a follow-up question, use the
conversation history to understand the reference.

5. Give clear, professional answers.

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


        return await self.conversation_service.create_conversation(
            db=db,
            user_id=user_id,
            title=question[:60],
        )