"""
add user settings

Revision ID: 925891f6083e
Revises: 5fd4ae23b7dd
Create Date: 2026-07-30 14:32:37.440112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "925891f6083e"
down_revision: Union[str, Sequence[str], None] = "5fd4ae23b7dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "settings",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "ai_provider",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "chat_model",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "embedding_model",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "top_k",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "similarity_threshold",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "temperature",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "max_tokens",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "system_prompt",
            sa.String(length=4000),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )


    op.create_index(
        op.f("ix_settings_user_id"),
        "settings",
        ["user_id"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_settings_user_id"),
        table_name="settings",
    )

    op.drop_table(
        "settings",
    )