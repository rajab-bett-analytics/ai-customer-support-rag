from enum import Enum


class Intent(str, Enum):
    """
    Supported user intents.
    """

    GREETING = "greeting"

    IDENTITY = "identity"

    CAPABILITIES = "capabilities"

    THANKS = "thanks"

    GOODBYE = "goodbye"

    GENERAL = "general"

    DOCUMENT_QUERY = "document_query"