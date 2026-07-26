"""
PDF utility functions.

Provides helper functions for extracting structured text
from PDF documents using PyMuPDF.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from pathlib import Path

import fitz


def extract_text_from_pdf(
    file_path: str | Path,
) -> list[dict[str, int | str]]:
    """
    Extract text from each page of a PDF.

    Args:
        file_path: Path to the PDF document.

    Returns:
        A list containing one dictionary per page.

        Example:
        [
            {
                "page": 1,
                "text": "Page one text..."
            },
            {
                "page": 2,
                "text": "Page two text..."
            }
        ]
    """

    document = fitz.open(file_path)

    pages: list[dict[str, int | str]] = []

    try:

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            text = page.get_text(
                "text",
                sort=True,
            ).strip()

            if not text:
                continue

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    finally:
        document.close()

    return pages