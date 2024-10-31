from datetime import datetime, timezone
from typing import Optional

import reflex as rx
from sqlmodel import Column, DateTime, Field, func


class User(rx.Model, table=True):
    """store customer information"""

    email: str


class Payment(rx.Model, table=True):
    """store payment information from stripe checkout"""

    id: int
    amount: int  # in cents
    status: str
    user_email: Optional[str] = Field(foreign_key="user.email")

    # timezones related
    created: datetime = Field(
        datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    updated: datetime = Field(
        datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )

    def dict(self, *args, **kwargs) -> dict:
        """Serialize method."""
        d = super().dict(*args, **kwargs)
        d["created"] = self.created.replace(microsecond=0).isoformat()
        d["updated"] = self.updated.replace(microsecond=0).isoformat()
        return d


def setup_admin_dash(app: rx.App):
    """
    Setup the admin dashboard.
    can pass as an arg to App instantiation like:

    app = rx.App(
        admin_dash=rx.AdminDash(models=[Customer]),
    )

    or use this function to set it up later.

    """
    app.admin_dash = rx.AdminDash(models=[User, Payment])
    return app
