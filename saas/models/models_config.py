from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from saas.rxext.utils.token_utils import hash_token


class TableConfig:
    class MagicLinkConfig:
        """Configuration for magic link authentication"""

        DEFAULT_RATE_LIMIT: int = 5  # max attempts allowed
        DEFAULT_EXPIRATION: timedelta = timedelta(minutes=60)  # link validity period
        MAX_ATTEMPTS: int = 5  # max attempts before link is invalid

        _token_hashed: bool = False

        @classmethod
        def default_expiration(cls) -> datetime:
            """Returns default expiration time from now"""
            return datetime.now(timezone.utc) + cls.DEFAULT_EXPIRATION


def generate_token_factory():
    """
    its possible you may want to encode the token itself in which case you will need to verify the token
    """
    token = token_urlsafe()
    if TableConfig.MagicLinkConfig._token_hashed:
        token = hash_token(token)

    return token
