"""
Intent service.

Uses Gemini to classify user messages into supported
intents before they are processed by the chat service.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

import json

from google import genai

from backend.core.config import settings
from backend.core.enums.intent import Intent
from backend.schemas.intent import IntentResult


class IntentService:
    """
    AI-powered intent classification service.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    async def classify(
        self,
        message: str,
    ) -> IntentResult:
        """
        Classify a user message using Gemini.

        Args:
            message: User input.

        Returns:
            Intent classification result.
        """

        prompt = f"""
You are an AI intent classification system.

Your task is to classify a user's message into EXACTLY ONE
of the following intents.

Allowed intents:

- GREETING
- IDENTITY
- CAPABILITIES
- THANKS
- GOODBYE
- DOCUMENT_QUERY
- GENERAL

Intent meanings:

GREETING
The user is greeting, starting a conversation,
or using informal greetings or slang.

Examples include messages like:
hello
hi
hey
hey there
good morning
good afternoon
good evening
greetings
sasa
mambo
niaje
yo

IDENTITY
The user wants to know who or what the assistant is.

CAPABILITIES
The user asks what the assistant can do,
how it can help,
or what features it has.

THANKS
The user is expressing gratitude.

GOODBYE
The user is ending the conversation.

DOCUMENT_QUERY
The user is requesting information that must be
looked up from uploaded documents, such as
contracts,
leave,
salary,
policies,
employment,
manuals,
PDFs,
agreements,
benefits,
procedures,
or similar knowledge-base content.

GENERAL
General conversation that is not a greeting,
identity question,
capability question,
thanks,
goodbye,
or document lookup.

Respond ONLY with valid JSON.

Format:

{{
    "intent": "GREETING",
    "confidence": 0.98
}}

User message:

"{message}"
"""

        try:

            response = self.client.models.generate_content(
                model=settings.CHAT_MODEL,
                contents=prompt,
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = (
                    text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            data = json.loads(text)

            return IntentResult(
                intent=Intent(
                    data["intent"].lower()
                ),
                confidence=float(
                    data.get(
                        "confidence",
                        0.80,
                    )
                ),
            )

        except Exception:

            return IntentResult(
                intent=Intent.GENERAL,
                confidence=0.50,
            )