import pytest
import base64
import cryptography
import time
from blockchain import Blockchain, Transaction, Block

@pytest.fixture(params=cryptography.SUPPORTED_SIGNATURE_ALGORITHMS)
def init(request):
    signature_algorithm = request.param
    crypto_provider = cryptography.CryptoProvider(signature_algorithm, 'sha512')
    public_key1, secret_key1 = crypto_provider.generate_keypair()
    address1 = base64.b64encode(public_key1).decode("utf-8")
    public_key2, secret_key2 = crypto_provider.generate_keypair()
    address2 = base64.b64encode(public_key2).decode("utf-8")
    
    # Create transactions
    transaction1 = Transaction(address1, address2, 30, crypto_provider)
    transaction1.sign_transaction(secret_key1)
    transaction2 = Transaction(address2, address1, 10, crypto_provider)
    transaction2.sign_transaction(secret_key2)
    transaction3 = Transaction(address2, address1, 15, crypto_provider)
    transaction3.sign_transaction(secret_key2)
    
    #Create blockchain and add transactions
    blockchain = Blockchain(2, 1, crypto_provider)
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)
    blockchain.add_transaction(transaction3)

    return blockchain, address1, address2

def test_add_and_mine_transactions(init):
    blockchain, address1, address2 = init

    assert blockchain.get_balance(address1) == 0, "Balance of address1 should be 0"
    assert blockchain.get_balance(address2) == 0, "Balance of address2 should be 0"

    blockchain.mine_pending_transactions()
    assert blockchain.get_balance(address1) == -20, "Balance of address1 should be -5"
    assert blockchain.get_balance(address2) == 20, "Balance of address2 should be 5"

    blockchain.mine_pending_transactions()
    assert blockchain.get_balance(address1) == -5, "Balance of address1 should be -5"
    assert blockchain.get_balance(address2) == 5, "Balance of address2 should be 5"

    ret = blockchain.mine_pending_transactions()
    assert ret == "No transactions to mine.", "Mining should return info when there are no pending transactions"

def test_is_valid(init):
    blockchain, address1, address2 = init

    assert blockchain.is_valid() == True, "Blockchain should be valid"

    blockchain.mine_pending_transactions()
    assert blockchain.is_valid() == True, "Blockchain should be valid even after mining the first block"

    blockchain.chain[1].transactions[0].amount = 100
    assert blockchain.is_valid() == False, "Blockchain should be invalid after modifying a transaction"