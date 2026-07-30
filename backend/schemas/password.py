"""
Password schemas.

Defines request models for password management.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class PasswordChange(BaseModel):
    """
    Request schema for changing the authenticated
    user's password.
    """

    current_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
        ),
    ]

    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
        ),
    ]

    confirm_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
        ),
    ]

    @model_validator(mode="after")
    def validate_passwords(self) -> "PasswordChange":
        """
        Ensure the new password and confirmation match.
        """

        if self.new_password != self.confirm_password:
            raise ValueError(
                "New password and confirmation password do not match."
            )

        return self