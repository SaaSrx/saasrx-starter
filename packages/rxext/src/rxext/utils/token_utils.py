import bcrypt

_SALT_ROUNDS = 6  # default is 12


def _ensure_bytes(value: bytes | str) -> bytes:
    """
    Ensure the input value is in bytes format.

    Args:
        value (bytes | str): The input value which can be either bytes or string.

    Returns:
        bytes: The input value converted to bytes if it was a string, otherwise returns the original bytes value.
    """
    if isinstance(value, str):
        return value.encode("utf-8")
    return value


def hash_token(token: str, *, salt: bytes | None = None) -> bytes:
    """Hash the token using bcrypt.

    Args:
        token: The password to hash.

    Returns:
        The hashed token.
    """

    return bcrypt.hashpw(
        password=_ensure_bytes(token),
        salt=salt or bcrypt.gensalt(rounds=_SALT_ROUNDS),
    )


def verify(token: str, hashed_password: bytes | str) -> bool:
    """Validate the otp_hash.

    Args:
        token: The password to check.

    Returns:
        True if the hashed token matches this user's otp_hash.
    """
    return bcrypt.checkpw(
        password=_ensure_bytes(token),
        hashed_password=_ensure_bytes(hashed_password),
    )
