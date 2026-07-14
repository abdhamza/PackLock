import pytest

from packlock.crypto import DecryptionError, decrypt, encrypt


def test_encrypt_decrypt_roundtrip():
    data = b"secret payload"
    password = "correct horse battery staple"

    blob = encrypt(data, password)

    assert decrypt(blob, password) == data


def test_decrypt_wrong_password_raises():
    blob = encrypt(b"top secret", "right-password")

    with pytest.raises(DecryptionError):
        decrypt(blob, "wrong-password")


def test_decrypt_rejects_garbage_input():
    with pytest.raises(DecryptionError):
        decrypt(b"not a vault", "password")


def test_encrypt_uses_random_salt_and_nonce():
    data = b"same input"
    password = "same password"

    assert encrypt(data, password) != encrypt(data, password)
