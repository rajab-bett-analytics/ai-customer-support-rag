"""
Text chunking utilities.

Splits extracted PDF pages into overlapping chunks while
preserving page numbers.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from collections.abc import Sequence


def chunk_text(
    pages: Sequence[dict[str, int | str]],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict[str, int | str]]:
    """
    Split extracted PDF pages into overlapping chunks.

    Args:
        pages:
            List of dictionaries returned by
            extract_text_from_pdf().

        chunk_size:
            Maximum characters per chunk.

        overlap:
            Number of overlapping characters.

    Returns:
        Example:

        [
            {
                "page": 1,
                "chunk_index": 0,
                "text": "..."
            },
            {
                "page": 1,
                "chunk_index": 1,
                "text": "..."
            }
        ]
    """

    chunks: list[dict[str, int | str]] = []

    chunk_index = 0

    for page in pages:

        page_number = int(page["page"])
        text = str(page["text"]).strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:

                chunks.append(
                    {
                        "page": page_number,
                        "chunk_index": chunk_index,
                        "text": chunk,
                    }
                )

                chunk_index += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks