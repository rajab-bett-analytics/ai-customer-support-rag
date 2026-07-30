"""
Generation service.

Generates AI responses for both general conversations
and Retrieval-Augmented Generation (RAG).

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from google import genai
from google.genai.types import GenerateContentConfig

from backend.core.config import settings
from backend.core.exceptions import AIServiceError
from backend.core.logger import get_logger
from backend.models.settings import Settings


logger = get_logger(__name__)


class GenerationService:
    """
    Handles AI text generation for:

    - General conversations
    - Retrieval-Augmented Generation (RAG)

    Supports user-configurable AI settings.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    async def generate(
        self,
        history: str,
        question: str,
        user_settings: Settings,
    ) -> str:
        """
        Generate a general conversational response.
        """

        system_prompt = (
            user_settings.system_prompt
            or "You are a helpful AI Customer Support Assistant."
        )

        prompt = f"""
{system_prompt}

The user's message does NOT require searching
uploaded documents.

Your task is to respond naturally and professionally.

Allowed:

- greet users
- introduce yourself
- explain your capabilities
- answer thanks
- answer goodbyes
- handle simple conversation

Rules:

- Be friendly and concise.
- Keep responses under 100 words.
- Never invent company information.
- Never create fake policies.
- Never answer document questions.

If the question requires uploaded documents,
reply ONLY:

DOCUMENT_QUERY

==================================================
CONVERSATION HISTORY
==================================================

{history}

==================================================
USER MESSAGE
==================================================

{question}

==================================================
ASSISTANT
==================================================
"""

        logger.info(
            "Generating general AI response."
        )

        return await self._generate(
            prompt=prompt,
            user_settings=user_settings,
        )

    async def generate_rag(
        self,
        prompt: str,
        user_settings: Settings,
    ) -> str:
        """
        Generate response using retrieved documents.
        """

        logger.info(
            "Generating RAG response."
        )

        return await self._generate(
            prompt=prompt,
            user_settings=user_settings,
        )

    async def _generate(
        self,
        prompt: str,
        user_settings: Settings,
    ) -> str:
        """
        Select AI provider.
        """

        provider = (
            user_settings.ai_provider
            or "google"
        ).strip().lower()

        logger.info(
            "AI Provider: %s",
            provider,
        )

        if provider in (
            "google",
            "gemini",
            "google gemini",
            "google-gemini",
        ):
            return await self._generate_gemini(
                prompt=prompt,
                user_settings=user_settings,
            )

        if provider == "openai":
            raise NotImplementedError(
                "OpenAI provider is not implemented yet."
            )

        if provider in (
            "anthropic",
            "claude",
        ):
            raise NotImplementedError(
                "Anthropic provider is not implemented yet."
            )

        raise AIServiceError(
            f"Unsupported AI provider: {provider}"
        )

    async def _generate_gemini(
        self,
        prompt: str,
        user_settings: Settings,
    ) -> str:
        """
        Generate response using Google Gemini.
        """

        try:

            response = self.client.models.generate_content(
                model=(
                    user_settings.chat_model
                    or settings.CHAT_MODEL
                ),
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=(
                        user_settings.temperature
                        or 0.3
                    ),
                    max_output_tokens=(
                        user_settings.max_tokens
                        or 1024
                    ),
                ),
            )

            answer = (
                response.text.strip()
                if response.text
                else ""
            )

            if not answer:
                raise AIServiceError(
                    "AI returned an empty response."
                )

            logger.info(
                "Gemini response generated successfully."
            )

            return answer

        except AIServiceError:
            raise

        except Exception as exc:

            logger.exception(
                "Gemini generation failed."
            )

            raise AIServiceError(
                "Unable to generate AI response."
            ) from exc