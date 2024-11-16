import os

import reflex as rx

from saas.app_config import config
from saas.models import AccessLevel, User

admin_email = os.environ.get("admin_email")


def seed_db():
    admin_user = User(
        email=admin_email,
        access_level=AccessLevel.ADMIN,
        is_admin=True,
    )

    with rx.session(config.db_url) as session:
        session.add(admin_user)
        session.commit()


if __name__ == "__main__":
    seed_db()
