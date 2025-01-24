"""Database seeding utility for SaaSRX.

This script provides functionality to seed the database with users of different access levels.
It can be run from the command line with various options to create users with specific
access levels and email addresses.

Usage:
    # Create a user with default settings (admin user with default email)
    python scripts/dbseed.py

    # Create a user with specific email and access level
    python scripts/dbseed.py --email user@example.com --access-level FULL_ACCESS

    # Available access levels: ADMIN, FULL_ACCESS, NO_PAYMENT
"""

import os
from typing import Optional

import reflex as rx
import typer
from sqlmodel import select

from saas.app_config import config, secrets
from saas.models import AccessLevel, User

email_default = os.environ.get("admin_email", secrets.admin_email)


def seed_db_user(
    email: str = email_default,
    access_level: AccessLevel = AccessLevel.ADMIN,
    quiet: bool = False,
) -> None:
    """Seed the database with a user.

    Args:
        email: Email address for the user. Defaults to admin_email from environment or secrets.
        access_level: Access level for the user. Defaults to ADMIN.
        quiet: If True, suppress output messages. Defaults to False.

    Raises:
        ValueError: If attempting to create a non-admin user with an existing admin email.
    """
    with rx.session(config.db_url) as session:
        # Check if user already exists
        if existing_user := session.exec(select(User).where(User.email == email)).one_or_none():
            if existing_user.is_admin and access_level != AccessLevel.ADMIN:
                raise ValueError(f"User with email {email} already exists as admin.")
            if not quiet:
                print(f"User with email {email} already exists. Skipping creation.")
            return

        user = User(email=email, access_level=access_level)
        if not quiet:
            print(f"Adding user: {user=}")
        session.add(user)
        session.commit()


def seed_all_access_levels(base_email: str = "user@example.com", quiet: bool = False) -> None:
    """Seed the database with one user for each access level.

    Args:
        base_email: Base email address to use. Will be modified for each access level.
        quiet: If True, suppress output messages.
    """
    for level in AccessLevel:
        email = f"{level.lower()}_{base_email}"
        try:
            seed_db_user(email=email, access_level=level, quiet=quiet)
            if not quiet:
                print(f"Created {level} user: {email}")
        except Exception as e:
            print(f"Error creating {level} user: {e}")


if __name__ == "__main__":
    app = typer.Typer()

    @app.command()
    def add_user(
        email: Optional[str] = typer.Option(
            email_default,
            "--email",
            "-e",
            help="Email address for the user",
        ),
        access_level: AccessLevel = typer.Option(
            AccessLevel.ADMIN,
            "--access-level",
            "-a",
            help="Access level for the user",
        ),
        quiet: bool = typer.Option(
            False,
            "--quiet",
            "-q",
            help="Suppress output messages",
        ),
    ):
        """Add a single user to the database."""
        seed_db_user(email, access_level, quiet)

    @app.command()
    def add_all_levels(
        base_email: str = typer.Option(
            "user@example.com",
            "--base-email",
            "-b",
            help="Base email address for generated users",
        ),
        quiet: bool = typer.Option(
            False,
            "--quiet",
            "-q",
            help="Suppress output messages",
        ),
    ):
        """Add one user for each access level."""
        seed_all_access_levels(base_email, quiet)

    app()
