"""
Chapter 10: Security — Authentication & Password Hashing

Demonstrates secure password handling with bcrypt,
JWT-like token generation, and input validation.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import base64
import secrets
import time
import re

# ── Password Hashing (Chapter 10: Defence in Depth) ────────────

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    _HAS_BCRYPT = False


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Chapter 10: NEVER store passwords in plain text.
    bcrypt automatically handles salting and is intentionally slow
    to resist brute-force attacks.

    Args:
        password: The plain-text password.

    Returns:
        The hashed password string.
    """
    if _HAS_BCRYPT:
        return bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
    # Fallback for environments without bcrypt (uses SHA-256 + salt)
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"sha256:{salt}:{hashed}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash.

    Args:
        password: The plain-text password to verify.
        hashed: The stored hash.

    Returns:
        True if the password matches.
    """
    if _HAS_BCRYPT and hashed.startswith("$2"):
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed.encode("utf-8")
        )
    # Fallback verification
    if hashed.startswith("sha256:"):
        _, salt, expected = hashed.split(":")
        actual = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return hmac.compare_digest(actual, expected)
    return False


# ── Token Generation (Chapter 10: JWT simplified) ───────────────

_SECRET_KEY = secrets.token_hex(32)  # In production: load from env var


def create_token(user_id: int, username: str, ttl_seconds: int = 3600) -> str:
    """Create a simple signed token (JWT-like structure).

    Chapter 10: Tokens are SIGNED, not encrypted.
    Anyone can decode the payload — the signature proves integrity.

    Args:
        user_id: The authenticated user's ID.
        username: The authenticated user's username.
        ttl_seconds: Token lifetime in seconds (default: 1 hour).

    Returns:
        A Base64-encoded token string: header.payload.signature
    """
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": int(time.time()) + ttl_seconds,
        "iat": int(time.time()),
    }

    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header).encode()
    ).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(payload).encode()
    ).decode().rstrip("=")

    signature = hmac.new(
        _SECRET_KEY.encode(),
        f"{header_b64}.{payload_b64}".encode(),
        hashlib.sha256,
    ).hexdigest()

    return f"{header_b64}.{payload_b64}.{signature}"


def verify_token(token: str) -> dict | None:
    """Verify a token's signature and expiration.

    Returns:
        The payload dict if valid, None if invalid or expired.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature = parts

        expected_sig = hmac.new(
            _SECRET_KEY.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return None

        # Pad base64 if needed
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding

        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        if payload.get("exp", 0) < time.time():
            return None

        return payload
    except Exception:
        return None


# ── Input Validation (Chapter 10: Defence in Depth) ─────────────

def validate_email(email: str) -> bool:
    """Basic email format validation.

    Chapter 10: Validate inputs at every boundary.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input.

    Chapter 10: Defence in depth — sanitize even after validation.
    """
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove script-like patterns
    text = re.sub(r"(?i)(javascript|onerror|onload|onclick):", "", text)
    return text.strip()
