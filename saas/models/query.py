import reflex as rx
from sqlmodel import func

from saas.models.schema import MagicLink, User, Payment


def find_user_by_email(email: str) -> User | None:
    """
    Retrieve a user from the database based on their email address.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    with rx.session() as session:
        user: User | None = session.exec(User.select().where(User.email == email.lower())).one_or_none()
    return user


def get_magic_link_token(user: User) -> str:
    """
    Retrieve or create a magic link for the given user.

    This function attempts to find an existing valid magic link for the user.
    If a valid magic link is found, it decrements the attempts remaining.
    If no valid magic link is found, it creates a new one.
    The function then commits the changes to the database and returns the token of the magic link.

    Note: if returning the magic link, you may need to use session.refresh and seperate the creation/update.
        right now just using a more efficient less verbose approach

    Args:
        user (User): The user for whom the magic link is being retrieved or created.

    Returns:
        str: The token of the retrieved or newly created magic link.
    """

    with rx.session() as session:
        magic_link = session.exec(
            MagicLink.select().where(
                MagicLink.user_email == user.email,
                MagicLink.valid_link(),
            )
        ).first()

        if magic_link:
            magic_link.attempts_remaining -= 1
        else:
            magic_link = MagicLink(user_email=user.email, user=user)
        token = magic_link.token

        session.add(magic_link)
        session.commit()
        return token


def check_magic_link(email: str, token: str, _return_bool: bool = False) -> MagicLink | bool:
    """
    Verifies the validity of a magic link based on the provided email and token.

    Args:
        email (str): The email address associated with the magic link.
        token (str): The token associated with the magic link.

    Returns:
        bool: True if a valid magic link is found, False otherwise.
    """
    with rx.session() as session:
        magic_link = session.exec(
            MagicLink.select()
            .where(
                MagicLink.user_email == email.lower(),
                MagicLink.expiration >= func.now(),
                MagicLink.token == token,
            )
            .order_by(MagicLink.created.desc())
            .limit(1),
        ).one_or_none()

        if _return_bool:
            return magic_link is not None

        return magic_link


def get_user_payments(user_email: str) -> list:
    """
    Retrieve all payments for a user from the database.

    Args:
        user_email (str): The email address of the user.

    Returns:
        list: A list of Payment objects for the user, ordered by creation date descending.
    """
    with rx.session() as session:
        payments = session.exec(
            Payment.select()
            .where(Payment.user_email == user_email)
            .order_by(Payment.created.desc())
        ).all()
        return payments
