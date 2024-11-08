import pytest

from saas.rxext.utils.token_utils import _ensure_bytes, hash_token, verify


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("test", b"test"),
        (b"test", b"test"),
    ],
)
def test_ensure_bytes(input_value, expected_output):
    assert _ensure_bytes(input_value) == expected_output


def test_hash_token():
    token = "test_token"
    hashed = hash_token(token)
    assert isinstance(hashed, bytes)
    assert hashed != _ensure_bytes(token)


def test_verify_success():
    token = "test_token"
    hashed = hash_token(token)
    assert verify(token, hashed)


def test_verify_failure():
    token = "test_token"
    hashed = hash_token(token)
    assert not verify("wrong_token", hashed)
