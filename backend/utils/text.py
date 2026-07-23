"""
Text utility functions.

Provides helper functions for cleaning and preparing
text before chunking and embedding generation.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    Removes excessive whitespace while preserving
    paragraph breaks.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove tabs
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()