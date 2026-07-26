from pydantic import BaseModel

from backend.core.enums.intent import Intent


class IntentResult(BaseModel):
    """
    Result returned by the intent classifier.
    """

    intent: Intent

    confidence: float

    response: str | None = None