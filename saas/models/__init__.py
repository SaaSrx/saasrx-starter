from datetime import datetime, timezone
from typing import Optional

import reflex as rx
from sqlmodel import JSON, Column, DateTime, Field, func


class User(rx.Model, table=True):
    """store customer information"""

    email: str = Field(primary_key=True, unique=True)


class MagicLinkAuth(rx.Model, table=True):
    """Store magic link authentication tokens"""

    # email: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(index=True)
    attempts: int = Field(default=0)  # Track number of attempts
    created: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    expiration: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    last_attempt: Optional[datetime] = Field(default=None)  # Track last attempt time


# class Payment(rx.Model, table=True):
#     """store payment information from stripe checkout"""

#     id: int
#     amount: int  # in cents
#     status: str  # pending, completed, refunded

#     user_email: Optional[str] = Field(foreign_key="user.email")
#     data: dict = Field(sa_column=Column(JSON), default={})

#     # timezones related
#     created: datetime = Field(
#         datetime.now(timezone.utc),
#         sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
#     )

#     updated: datetime = Field(
#         datetime.now(timezone.utc),
#         sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
#     )

#     def dict(self, *args, **kwargs) -> dict:
#         """Serialize method."""
#         d = super().dict(*args, **kwargs)
#         d["created"] = self.created.replace(microsecond=0).isoformat()
#         d["updated"] = self.updated.replace(microsecond=0).isoformat()
#         return d


def setup_admin_dash(app: rx.App, tables: list[rx.Model] = None):
    """
    Setup the admin dashboard.
    can pass as an arg to App instantiation like:

    app = rx.App(
        admin_dash=rx.AdminDash(models=[Customer]),
    )

    or use this function to set it up later.

    """
    tables = tables or [User, MagicLinkAuth]
    app.admin_dash = rx.AdminDash(models=tables)
    return app
