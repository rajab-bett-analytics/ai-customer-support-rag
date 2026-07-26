"""
Generation service.

Generates conversational AI responses that do not require
Retrieval-Augmented Generation (RAG).

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from google import genai

from backend.core.config import settings
from backend.core.exceptions import AIServiceError
from backend.core.logger import get_logger


logger = get_logger(__name__)


class GenerationService:
    """
    Handles general AI conversations that do not require
    document retrieval.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    async def generate(
        self,
        history: str,
        question: str,
    ) -> str:
        """
        Generate a conversational response.

        Args:
            history: Conversation history.
            question: User message.

        Returns:
            AI-generated response.
        """

        prompt = f"""
You are an AI Customer Support Assistant.

The user's message does NOT require searching
uploaded documents.

Your job is to respond naturally and professionally.

You can:

- greet users
- introduce yourself
- explain your capabilities
- answer thanks
- answer goodbyes
- engage in simple conversation

Guidelines:

- Be friendly and concise.
- Keep responses under 100 words.
- Do not invent company policies.
- Do not answer questions that require searching
  uploaded documents.
- If the user's question requires searching
  documents, reply ONLY with:

DOCUMENT_QUERY

Conversation History:
{history}

User:
{question}

Assistant:
"""

        logger.info(
            "Generating conversational response."
        )

        try:

            response = self.client.models.generate_content(
                model=settings.CHAT_MODEL,
                contents=prompt,
            )

            answer = response.text.strip()

            logger.info(
                "Conversational response generated successfully."
            )

            return answer

        except Exception as exc:

            logger.exception(
                "Failed to generate conversational response."
            )

            raise AIServiceError(
                "Unable to generate AI response."
            ) from exc