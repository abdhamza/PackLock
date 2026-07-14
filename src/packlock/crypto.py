"""AES-256-GCM encryption primitives for PackLock vault files.

Vault file layout:
    MAGIC (4 bytes) | VERSION (1 byte) | SALT (16 bytes) | NONCE (12 bytes) | CIPHERTEXT
"""

from __future__ import annotations

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b"PLCK"
VERSION = 1

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # AES-256
# OWASP (2023) minimum recommendation for PBKDF2-HMAC-SHA256.
KDF_ITERATIONS = 600_000

_HEADER_SIZE = len(MAGIC) + 1 + SALT_SIZE + NONCE_SIZE


class DecryptionError(Exception):
    """Raised when a vault cannot be decrypted (wrong password or corrupted file)."""


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(data: bytes, password: str) -> bytes:
    """Encrypt ``data`` into a self-contained PackLock vault blob."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = _derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, data, associated_data=None)
    return MAGIC + bytes([VERSION]) + salt + nonce + ciphertext


def decrypt(blob: bytes, password: str) -> bytes:
    """Decrypt a PackLock vault blob produced by :func:`encrypt`.

    Raises:
        DecryptionError: if the blob is malformed, uses an unsupported
            version, or the password is wrong / data has been tampered with.
    """
    if len(blob) < _HEADER_SIZE or blob[: len(MAGIC)] != MAGIC:
        raise DecryptionError("Not a valid PackLock vault file.")

    offset = len(MAGIC)
    version = blob[offset]
    offset += 1
    if version != VERSION:
        raise DecryptionError(f"Unsupported vault version: {version}")

    salt = blob[offset : offset + SALT_SIZE]
    offset += SALT_SIZE
    nonce = blob[offset : offset + NONCE_SIZE]
    offset += NONCE_SIZE
    ciphertext = blob[offset:]

    key = _derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, associated_data=None)
    except InvalidTag as exc:
        raise DecryptionError("Incorrect password or corrupted vault file.") from exc
