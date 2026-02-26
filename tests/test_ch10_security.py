"""Tests for Chapter 10: Security — Authentication"""
import pytest
from horizon.auth import (
    hash_password, verify_password,
    create_token, verify_token,
    validate_email, sanitize_input,
)


class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        hashed = hash_password("s3cret!")
        assert hashed != "s3cret!"

    def test_verify_correct_password(self):
        hashed = hash_password("s3cret!")
        assert verify_password("s3cret!", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("s3cret!")
        assert verify_password("wrong!", hashed) is False

    def test_different_hashes_for_same_password(self):
        h1 = hash_password("s3cret!")
        h2 = hash_password("s3cret!")
        # Salted hashes should differ
        assert h1 != h2


class TestTokens:
    def test_create_and_verify_token(self):
        token = create_token(user_id=42, username="amara")
        payload = verify_token(token)
        assert payload is not None
        assert payload["user_id"] == 42
        assert payload["username"] == "amara"

    def test_token_has_three_parts(self):
        token = create_token(user_id=1, username="test")
        assert len(token.split(".")) == 3

    def test_expired_token_rejected(self):
        token = create_token(user_id=1, username="test", ttl_seconds=-1)
        assert verify_token(token) is None

    def test_tampered_token_rejected(self):
        token = create_token(user_id=1, username="test")
        # Tamper with the payload
        parts = token.split(".")
        parts[1] = parts[1][::-1]  # Reverse it
        tampered = ".".join(parts)
        assert verify_token(tampered) is None

    def test_invalid_format_rejected(self):
        assert verify_token("not.a.valid.token.at.all") is None
        assert verify_token("garbage") is None


class TestInputValidation:
    def test_valid_emails(self):
        assert validate_email("amara@horizon.app") is True
        assert validate_email("user.name+tag@example.com") is True

    def test_invalid_emails(self):
        assert validate_email("") is False
        assert validate_email("no-at-sign") is False
        assert validate_email("@no-local.com") is False

    def test_sanitize_removes_html(self):
        assert sanitize_input("<script>alert('xss')</script>") == "alert('xss')"

    def test_sanitize_removes_event_handlers(self):
        result = sanitize_input("onerror:alert(1)")
        assert "onerror" not in result

    def test_sanitize_strips_whitespace(self):
        assert sanitize_input("  hello  ") == "hello"
