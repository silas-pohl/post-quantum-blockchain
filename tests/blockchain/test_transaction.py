import pytest
import base64
import cryptography
from blockchain import Transaction

algorithms = set(['Falcon-512'])

@pytest.fixture(params=cryptography.SUPPORTED_SIGNATURE_ALGORITHMS)
def init(request):
    signature_algorithm = request.param
    crypto_provider = cryptography.CryptoProvider(signature_algorithm, 'sha512')
    public_key1, secret_key1 = crypto_provider.generate_keypair()
    address1 = base64.b64encode(public_key1).decode("utf-8")
    public_key2, secret_key2 = crypto_provider.generate_keypair()
    address2 = base64.b64encode(public_key2).decode("utf-8")
    amount = 30
    transaction = Transaction(address1, address2, amount, crypto_provider)
    return transaction, address1, address2, amount, crypto_provider, secret_key1, secret_key2

def test_create_transaction(init):
    transaction, address1, address2, amount, crypto_provider, _, _ = init

    #Check if creation of transaction works
    assert isinstance(transaction, Transaction), "Transaction should be of type Transaction"
    assert transaction.sender == address1, "Sender should contain address1"
    assert transaction.recipient == address2, "Recipient should contain address2"
    assert transaction.amount == 30, "Amount should be 30"
    assert transaction.crypto_provider == crypto_provider, "Crypto Provider should be correct"
    assert transaction.signature is None, "On initialization, signature should be None"

def test_sign_and_verify_transaction(init):
    transaction, _, _, _, _, secret_key1, secret_key2 = init

    # Sign transaction with wrong secret key
    transaction.sign_transaction(secret_key2)
    assert isinstance(transaction.signature, bytes), "Signature should be bytes"
    is_valid = transaction.is_valid()
    assert not is_valid, "Transaction should not be valid after signing with wrong secret key"

    # Sign transaction with correct secret key
    transaction.sign_transaction(secret_key1)
    assert isinstance(transaction.signature, bytes), "Signature should be bytes"
    is_valid = transaction.is_valid()
    assert is_valid, "Transaction should be valid"

