"""Tests for the auth service (password hashing + JWT)."""
import time

from services import auth_service
from services.auth_service import (
    hash_password, verify_password, create_access_token, decode_access_token,
)


class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        h = hash_password("supersecret")
        assert h != "supersecret"
        assert h.startswith("$2")  # bcrypt prefix

    def test_verify_correct_password(self):
        h = hash_password("supersecret")
        assert verify_password("supersecret", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("supersecret")
        assert verify_password("wrong", h) is False

    def test_verify_handles_garbage_hash(self):
        assert verify_password("x", "not-a-hash") is False


class TestJWT:
    def test_create_and_decode_roundtrip(self):
        token = create_access_token({"sub": "42"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert "exp" in payload

    def test_decode_invalid_token_returns_none(self):
        assert decode_access_token("not.a.valid.token") is None
        assert decode_access_token("") is None

    def test_token_expiry_in_future(self):
        import datetime as dt
        token = create_access_token({"sub": "1"})
        payload = decode_access_token(token)
        exp = dt.datetime.fromtimestamp(payload["exp"], tz=dt.timezone.utc)
        assert exp > dt.datetime.now(dt.timezone.utc)
