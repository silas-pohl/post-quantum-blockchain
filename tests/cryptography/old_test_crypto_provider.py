import pytest
from cryptography import CryptoProvider

def test_ecdsa_keypair_generation():
    provider = CryptoProvider(signature_algorithm="ECDSA-SHA256", hashing_algorithm="sha256")
    public_key, secret_key = provider.generate_keypair()

    assert isinstance(public_key, bytes), "Public key should be bytes"
    assert isinstance(secret_key, bytes), "Secret key should be bytes"
    assert len(public_key) > 0, "Public key should not be empty"
    assert len(secret_key) > 0, "Secret key should not be empty"

def test_ecdsa_sign_and_verify():
    provider = CryptoProvider(signature_algorithm="ECDSA-SHA256", hashing_algorithm="sha256")
    public_key, secret_key = provider.generate_keypair()
    message = b"Test message for signing"

    # Sign the message
    signature = provider.sign(secret_key, message)
    assert isinstance(signature, bytes), "Signature should be bytes"
    assert len(signature) > 0, "Signature should not be empty"

    # Verify the signature
    is_valid = provider.verify(public_key, message, signature)
    assert is_valid, "Signature verification should return True"

    # Test with an invalid signature
    invalid_signature = signature[:-1] + b"\x00"  # Corrupt the signature
    is_valid = provider.verify(public_key, message, invalid_signature)
    assert not is_valid, "Verification of invalid signature should return False"

def test_oqs_keypair_generation_and_sign():
    provider = CryptoProvider(signature_algorithm="Dilithium2", hashing_algorithm="sha3_256")
    public_key, secret_key = provider.generate_keypair()

    assert isinstance(public_key, bytes), "Public key should be bytes"
    assert isinstance(secret_key, bytes), "Secret key should be bytes"
    assert len(public_key) > 0, "Public key should not be empty"
    assert len(secret_key) > 0, "Secret key should not be empty"

    message = b"Test message for OQS signing"

    # Sign the message
    signature = provider.sign(secret_key, message)
    assert isinstance(signature, bytes), "Signature should be bytes"
    assert len(signature) > 0, "Signature should not be empty"

    # Verify the signature
    is_valid = provider.verify(public_key, message, signature)
    assert is_valid, "OQS signature verification should return True"

def test_hashing():
    provider = CryptoProvider(signature_algorithm="ECDSA-SHA256", hashing_algorithm="sha256")
    data = b"Test data for hashing"

    hashed_data = provider.hash(data)
    assert isinstance(hashed_data, bytes), "Hashed data should be bytes"
    assert len(hashed_data) == 32, "SHA-256 hash length should be 32 bytes"

    provider = CryptoProvider(signature_algorithm="ECDSA-SHA256", hashing_algorithm="sha3_256")
    hashed_data = provider.hash(data)
    assert isinstance(hashed_data, bytes), "Hashed data should be bytes"
    assert len(hashed_data) == 32, "SHA3-256 hash length should be 32 bytes"
