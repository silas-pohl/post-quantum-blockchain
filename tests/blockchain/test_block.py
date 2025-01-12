import pytest
import base64
import cryptography
import time
from blockchain import Transaction, Block

@pytest.fixture(params=cryptography.SUPPORTED_SIGNATURE_ALGORITHMS)
def init(request):
    signature_algorithm = request.param
    crypto_provider = cryptography.CryptoProvider(signature_algorithm, 'sha512')
    public_key1, secret_key1 = crypto_provider.generate_keypair()
    address1 = base64.b64encode(public_key1).decode("utf-8")
    public_key2, secret_key2 = crypto_provider.generate_keypair()
    address2 = base64.b64encode(public_key2).decode("utf-8")
    amount1 = 30
    amount2 = 20
    transaction1 = Transaction(address1, address2, amount1, crypto_provider)
    transaction1.sign_transaction(secret_key1)
    transaction2 = Transaction(address2, address1, amount2, crypto_provider)
    transaction2.sign_transaction(secret_key2)
    timestamp = time.time()
    block = Block(0, "0", [transaction1, transaction2], crypto_provider, timestamp)

    return block, transaction1, transaction2, crypto_provider, timestamp

def test_create_block(init):
    block, transaction1, transaction2, crypto_provider, timestamp = init

    # Check if creation of block works
    assert isinstance(block, Block), "Block should be of type Block"
    assert block.index == 0, "Block index should be 0"
    assert block.previous_hash == "0", "Previous Hash should be 0-string"
    assert block.transactions == [transaction1, transaction2], "Transactions should be the list of the defined transactions"
    assert block.crypto_provider == crypto_provider, "CryptoProvider should be correct"
    assert block.timestamp == timestamp, "Timestamp should be timestamp of the creation of the block"
    assert block.hash is None, "Hash should be None before computation"

def test_compute_hash(init):
    block, _, _, crypto_provider, timestamp = init

    # Check correctness of hash calculation
    block_bytes = f'{block.index}{block.previous_hash}{block.transactions}{block.timestamp}{block.nonce}'.encode()
    block_hash = block.compute_hash()
    assert block_hash == crypto_provider.hash(block_bytes), "Compute hash should return the correct hash of the block"

def test_is_valid(init):
    block, _, _, crypto_provider, _ = init

    block.hash = block.compute_hash()

    # Check validity with valid transactions
    assert block.is_valid(), "Block should be valid"

    # Modify the amount of the first transaction to make the signature invalid
    block.transactions[0].amount = 0
    assert not block.is_valid(), "Block should not be valid after modifying the signature of one of the blocks transactions"