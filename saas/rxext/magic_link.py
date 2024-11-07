import secrets
from datetime import datetime, timedelta

import reflex as rx
from sqlmodel import delete, select

from rxconfig import config
from saas.models import MagicLinkAuth

default_expiration: timedelta = timedelta(minutes=60)
default_rate_limit: int = 5


class MagicLinkMixin:
    session_token: str = rx.LocalStorage(sync=True)

    def _check_recent(self, email: str, rate_limit: int, expiration_delta: timedelta) -> bool:
        """Check if user hasn't exceeded rate limit for magic link requests

        Args:
            email: The user's email
            rate_limit: Maximum number of attempts allowed
            expiration_delta: Time window for rate limiting

        Returns:
            bool: True if user can request another magic link
        """
        with rx.session() as session:
            # Get the most recent magic link record
            auth = session.get(MagicLinkAuth, email)
            if not auth:
                return True

            # Check if within rate limit window
            time_window = datetime.utcnow() - expiration_delta
            if auth.last_attempt and auth.last_attempt > time_window:
                if auth.attempts >= rate_limit:
                    return False

            # Reset attempts if outside window
            if auth.last_attempt and auth.last_attempt <= time_window:
                auth.attempts = 0
                session.commit()

            return True

    def _generate_link(
        self,
        email: str,
        expiration_delta: timedelta = default_expiration,
        rate_limit: int = default_rate_limit,
    ) -> str:
        """
        Generate a magic link for the account to allow user to click and login

        Args:
            email: The user's email address
            expiration_delta: How long the link should be valid for
            rate_limit: How many attempts are allowed

        Returns:
            str: The complete magic link URL
        """
        if not self._check_recent(email, rate_limit, expiration_delta):
            raise ValueError("Too many recent attempts. Please wait and try again.")

        # Generate a secure token
        token = secrets.token_urlsafe(32)
        expiration = datetime.utcnow() + expiration_delta

        # Store the token, email, and expiration in your database
        # This is a placeholder - implement your database storage
        self._store_magic_link(email, token, expiration)

        # Create the magic link URL
        base_url = f"http://{config.deploy_url}:{config.frontend_port}"  # Replace with your actual base URL
        magic_link = f"{base_url}/auth/verify?email={email}&token={token}"

        return magic_link

    def _validate_magic_link(self, email: str, token: str) -> bool:
        """
        Validate a magic link token

        Args:
            email: The user's email address
            token: The token to validate

        Returns:
            bool: True if the token is valid, False otherwise
        """
        # Get the stored token details from your database
        stored_token = self._get_stored_token(email)

        if not stored_token:
            return False

        # Check if token matches and hasn't expired
        if stored_token["token"] == token and datetime.utcnow() <= stored_token["expiration"]:
            # Token is valid - clean up the used token
            self._remove_token(email)
            return True

        return False

    def _store_magic_link(self, email: str, token: str, expiration: datetime):
        """Store magic link details in database

        Args:
            email: User's email
            token: Generated security token
            expiration: Token expiration timestamp
        """
        with rx.session() as session:
            # Get or create magic link record
            auth = session.get(MagicLinkAuth, email)
            if auth:
                auth.token = token
                auth.expiration = expiration
                auth.attempts += 1
                auth.last_attempt = datetime.utcnow()
            else:
                auth = MagicLinkAuth(
                    email=email,
                    token=token,
                    expiration=expiration,
                    attempts=1,
                    last_attempt=datetime.utcnow(),
                )
                session.add(auth)
            session.commit()

    def _get_stored_token(self, email: str) -> dict:
        """Get stored token details from database

        Args:
            email: User's email

        Returns:
            dict: Token details if found, None otherwise
        """
        with rx.session() as session:
            auth = session.get(MagicLinkAuth, email)
            if not auth:
                return None
            return {"token": auth.token, "expiration": auth.expiration}

    def _remove_token(self, email: str):
        """Remove used token from database

        Args:
            email: User's email
        """
        with rx.session() as session:
            session.execute(delete(MagicLinkAuth).where(MagicLinkAuth.email == email))
            session.commit()

    def send_magic_link(self, email: str) -> bool:
        """Public method to generate and send magic link

        Args:
            email: User's email

        Returns:
            bool: True if link was generated and sent successfully
        """
        try:
            magic_link = self._generate_link(email)
            # TODO: Implement email sending logic here
            # For now, just print the link
            print(f"Magic link generated: {magic_link}")
            return True
        except ValueError as e:
            print(f"Error generating magic link: {e}")
            return False


# class MagicLinkAuth(rx.State):
#     def on_load(self):
#         params = self.router.params
#         email = params.get("email")
#         token = params.get("token")
#         if not email or not token:
#             return rx.redirect("/signin")
#         token_valid = self._validate_magic_link(email, token)
#         if not token_valid:
#             return rx.redirect("/signin")

#         return rx.redirect("/dashboard")
