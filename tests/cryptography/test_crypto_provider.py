import pytest
import cryptography

@pytest.mark.parametrize("signature_algorithm", cryptography.SUPPORTED_SIGNATURE_ALGORITHMS)
def test_keygen_sign_and_verify(signature_algorithm):
    crypto_provider = cryptography.CryptoProvider(signature_algorithm, '')
    public_key, secret_key = crypto_provider.generate_keypair()

    assert isinstance(public_key, bytes), "Public key should be bytes"
    assert isinstance(secret_key, bytes), "Secret key should be bytes"
    assert len(public_key) > 0, "Public key should not be empty"
    assert len(secret_key) > 0, "Secret key should not be empty"

    message = b"Test message for signing"

    signature = crypto_provider.sign(secret_key, message)
    assert isinstance(signature, bytes), "Signature should be bytes"
    assert len(signature) > 0, "Signature should not be empty"

    is_valid = crypto_provider.verify(public_key, message, signature)
    assert is_valid, "Signature verification should return True"

    invalid_signature = signature[:-1] + bytes([signature[-1] ^ 0xFF]) # Corrupt the signature
    is_valid = crypto_provider.verify(public_key, message, invalid_signature)
    assert not is_valid, "Verification of invalid signature should return False"

@pytest.mark.parametrize("hash_function", cryptography.SUPPORTED_HASH_FUNCTIONS)
def test_hash(hash_function):

    # shake_128 and shake_256 have variable digest length, so they are as 'shake_128_x' and 'shake_256_x' in SUPPORTED_HASH_FUNCTIONS
    if hash_function.endswith('x'):
        hash_function = hash_function.replace('x', '20')

    crypto_provider = cryptography.CryptoProvider('', hash_function)
    data1 = b"Test data for hashing"
    data2 = b"Test data for hashing"
    data3 = b"Different test data for hashing"
    hashed_data1 = crypto_provider.hash(data1)
    hashed_data2 = crypto_provider.hash(data2)
    hashed_data3 = crypto_provider.hash(data3)
    assert isinstance(hashed_data1, bytes), "Hashed data should be bytes"
    assert hashed_data1 == hashed_data2, "Hashed data should be equal"
    assert hashed_data1 != hashed_data3, "Hashed data should not be equal"
