"""
PDF utility functions.

Provides helper functions for extracting text from PDF
documents using PyMuPDF.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pathlib import Path

import fitz


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract all text from a PDF document.

    Args:
        file_path: Path to the PDF.

    Returns:
        The extracted text.
    """

    document = fitz.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)