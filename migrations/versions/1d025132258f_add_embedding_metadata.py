"""Add embedding metadata

Revision ID: 1d025132258f
Revises: 47a8fdd28729
Create Date: 2026-07-26 22:28:16.476918
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1d025132258f"
down_revision: Union[str, Sequence[str], None] = "47a8fdd28729"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    # ---------------------------------------------------------
    # Add page metadata
    # ---------------------------------------------------------

    op.add_column(
        "embeddings",
        sa.Column(
            "page_number",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    # Remove temporary default after existing rows are populated
    op.alter_column(
        "embeddings",
        "page_number",
        server_default=None,
    )

    op.add_column(
        "embeddings",
        sa.Column(
            "section",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # Indexes
    # ---------------------------------------------------------

    op.create_index(
        "ix_embedding_document_page_chunk",
        "embeddings",
        [
            "document_id",
            "page_number",
            "chunk_index",
        ],
        unique=False,
    )

    op.create_index(
        op.f("ix_embeddings_page_number"),
        "embeddings",
        ["page_number"],
        unique=False,
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    op.drop_index(
        op.f("ix_embeddings_page_number"),
        table_name="embeddings",
    )

    op.drop_index(
        "ix_embedding_document_page_chunk",
        table_name="embeddings",
    )

    op.drop_column(
        "embeddings",
        "section",
    )

    op.drop_column(
        "embeddings",
        "page_number",
    )