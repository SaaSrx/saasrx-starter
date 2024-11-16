from datetime import datetime, timezone
from enum import StrEnum, auto
from secrets import token_hex
from typing import Optional

import reflex as rx
from sqlmodel import JSON, Column, DateTime, Field, func

from saas.models.models_config import TableConfig, generate_token_factory


class AccessLevel(StrEnum):
    """User access levels"""

    ADMIN = auto()
    FULL_ACCESS = auto()
    NO_PAYMENT = auto()


class User(rx.Model, table=True):
    """store customer information"""

    # email: str  # = Field(primary_key=True, unique=True)
    email: str = Field(unique=True)
    # access_level: int = Field(default=0)
    access_level: AccessLevel = Field(default=AccessLevel.NO_PAYMENT)
    is_admin: bool = Field(default=False)


class MagicLink(rx.Model, table=True):
    """Store magic link authentication tokens"""

    token: str = Field(default_factory=generate_token_factory)
    user_email: Optional[str] = Field(foreign_key="user.email")
    attempts_remaining: int = Field(default=TableConfig.MagicLinkConfig.MAX_ATTEMPTS)
    created: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    expiration: datetime = Field(
        default_factory=TableConfig.MagicLinkConfig.default_expiration,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    @classmethod
    def not_expired(cls):
        """Returns SQLAlchemy expression for checking if link is not expired"""
        return cls.expiration > func.now()

    @classmethod
    def valid_link(cls):
        """Returns SQLAlchemy expression for a valid link (not expired, less than max attempts)"""
        return (cls.expiration > func.now()) & (cls.attempts_remaining > 0)

    def get_session_token(self) -> str:
        return f"{self.token}:{token_hex()}"


class Payment(rx.Model, table=True):
    """store payment information from stripe checkout"""

    # id: int
    amount: int  # in cents
    status: str  # pending, completed, refunded

    user_email: str | None = Field(default=None, foreign_key="user.email")

    data: dict = Field(sa_column=Column(JSON), default={})

    # timezones related
    created: datetime = Field(
        datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    updated: datetime = Field(
        datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    def dict(self, *args, **kwargs) -> dict:
        """Serialize method."""
        d = super().dict(*args, **kwargs)
        d["created"] = self.created.replace(microsecond=0).isoformat()
        d["updated"] = self.updated.replace(microsecond=0).isoformat()
        return d
