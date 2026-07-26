"""
Application logging configuration.

Configures the global logging behavior for the
AI Customer Support RAG Platform.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

import logging


def configure_logging() -> None:
    """
    Configure the application's logging.

    This function should be called once during
    application startup.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )