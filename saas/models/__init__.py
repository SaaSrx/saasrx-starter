import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import Optional

import bcrypt
import reflex as rx
from sqlmodel import JSON, Column, DateTime, Field, Relationship, func


class TableConfig:
    class MagicLinkConfig:
        """Configuration for magic link authentication"""

        DEFAULT_RATE_LIMIT: int = 5  # max attempts allowed
        DEFAULT_EXPIRATION: timedelta = timedelta(minutes=60)  # link validity period
        MAX_ATTEMPTS: int = 5  # max attempts before link is invalid

        @classmethod
        def default_expiration(cls) -> datetime:
            """Returns default expiration time from now"""
            return datetime.now(timezone.utc) + cls.DEFAULT_EXPIRATION


class AccessLevel(Enum):
    """User access levels"""

    ADMIN = 0
    FULL_ACCESS = 1
    NO_PAYMENT = 2


class User(rx.Model, table=True):
    """store customer information"""

    # email: str  # = Field(primary_key=True, unique=True)
    email: str = Field(unique=True)
    # access_level: int = Field(default=0)
    access_level: AccessLevel = Field(default=AccessLevel.NO_PAYMENT)
    is_admin: bool = Field(default=False)


class MagicLink(rx.Model, table=True):
    """Store magic link authentication tokens"""

    token: str = Field(default_factory=secrets.token_urlsafe)
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

    @staticmethod
    def hash_token(token: str) -> bytes:
        """Hash the token using bcrypt.

        Args:
            token: The password to hash.

        Returns:
            The hashed token.
        """
        return bcrypt.hashpw(
            password=token.encode("utf-8"),
            salt=bcrypt.gensalt(),
        )

    def verify(self, token: str) -> bool:
        """Validate the otp_hash.

        Args:
            token: The password to check.

        Returns:
            True if the hashed token matches this user's otp_hash.
        """
        return bcrypt.checkpw(
            password=token.encode("utf-8"),
            hashed_password=self.otp_hash,
        )


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


Models = [
    User,
    MagicLink,
    Payment,
]


def setup_admin_dash(app: rx.App, tables: list[rx.Model] = None):
    """
    Setup the admin dashboard.
    can pass as an arg to App instantiation like:

    app = rx.App(
        admin_dash=rx.AdminDash(models=[Customer]),
    )

    or use this function to set it up later.

    """
    app.admin_dash = rx.AdminDash(models=tables or Models)
    return app
