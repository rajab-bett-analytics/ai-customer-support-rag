"""Add document processing metadata

Revision ID: 5fd4ae23b7dd
Revises: 1d025132258f
Create Date: 2026-07-27 14:32:42.483919
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5fd4ae23b7dd"
down_revision: Union[str, Sequence[str], None] = "1d025132258f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "page_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "chunk_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "embedding_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "indexed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "error_message",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "documents",
        "error_message",
    )

    op.drop_column(
        "documents",
        "indexed_at",
    )

    op.drop_column(
        "documents",
        "embedding_count",
    )

    op.drop_column(
        "documents",
        "chunk_count",
    )

    op.drop_column(
        "documents",
        "page_count",
    )