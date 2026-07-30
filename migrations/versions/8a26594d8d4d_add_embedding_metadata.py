"""add embedding metadata

Revision ID: 8a26594d8d4d
Revises: 925891f6083e
Create Date: 2026-07-30 21:40:41.195246

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8a26594d8d4d"
down_revision: Union[str, Sequence[str], None] = "925891f6083e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "embeddings",
        sa.Column(
            "embedding_model",
            sa.String(length=100),
            nullable=False,
            server_default="gemini-embedding-001",
        ),
    )

    op.add_column(
        "embeddings",
        sa.Column(
            "embedding_dimension",
            sa.Integer(),
            nullable=False,
            server_default="3072",
        ),
    )

    # Remove defaults so future inserts use your application values
    op.alter_column(
        "embeddings",
        "embedding_model",
        server_default=None,
    )

    op.alter_column(
        "embeddings",
        "embedding_dimension",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "embeddings",
        "embedding_dimension",
    )

    op.drop_column(
        "embeddings",
        "embedding_model",
    )