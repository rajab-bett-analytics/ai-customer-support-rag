"""
Custom application exceptions.

Defines domain-specific exceptions used throughout the
AI Customer Support RAG Platform.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""


class ApplicationError(Exception):
    """
    Base exception for all application-specific errors.
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(message)
        self.message = message


class AIServiceError(ApplicationError):
    """
    Raised when an AI provider cannot generate a response.
    """


class EmbeddingError(ApplicationError):
    """
    Raised when embedding generation fails.
    """


class RetrievalError(ApplicationError):
    """
    Raised when document retrieval fails.
    """


class DocumentProcessingError(ApplicationError):
    """
    Raised when a document cannot be processed.
    """


class IntentClassificationError(ApplicationError):
    """
    Raised when intent classification fails.
    """


class ConversationError(ApplicationError):
    """
    Raised when conversation operations fail.
    """


class AuthenticationError(ApplicationError):
    """
    Raised for authentication failures.
    """


class AuthorizationError(ApplicationError):
    """
    Raised for authorization failures.
    """