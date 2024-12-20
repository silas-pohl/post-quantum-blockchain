import cryptography
import base64
from blockchain import Transaction, Blockchain

#print(cryptography.SUPPORTED_SIGNATURE_ALGORITHMS)
#print(cryptography.SUPPORTED_HASH_FUNCTIONS)

algorithms = ['Falcon-512']


for algorithm in algorithms:
    crypto_provider = cryptography.CryptoProvider(algorithm,'sha512')
    private_key1, public_key1 = crypto_provider.generate_keypair()
    address1 = base64.b64encode(public_key1).decode("utf-8")
    decoded_public_key1 = base64.b64decode(address1)
    #print(public_key1 == decoded_public_key1)
    private_key2, public_key2 = crypto_provider.generate_keypair()
    address2 = base64.b64encode(public_key2).decode("utf-8")

    transaction1 = Transaction(address1, address2, 30, crypto_provider)
    transaction1.sign_transaction(private_key1)

    transaction2 = Transaction(address2, address1, 10, crypto_provider)
    transaction2.sign_transaction(private_key2)

    transaction3 = Transaction(address2, address1, 15, crypto_provider)
    transaction3.sign_transaction(private_key2)

    blockchain = Blockchain(2, 3, crypto_provider)
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)
    blockchain.add_transaction(transaction3)
    blockchain.mine_pending_transactions()

    #print(blockchain)

    print("\nChecking the balances of the addresses...")
    print(f"Balance of address1({address1}): {blockchain.get_balance(address1)}")
    print(f"Balance of address2({address2}): {blockchain.get_balance(address2)}")

    blockchain.mine_pending_transactions()
    print("\nMining the last pending transaction...")
    print("Checking the balances of the addresses again...")
    print(f"Balance of address1({address1}): {blockchain.get_balance(address1)}")
    print(f"Balance of address2({address2}): {blockchain.get_balance(address2)}")

    print("\nChecking the validity of the blockchain...")
    print(f"Blockchain validity: {blockchain.is_valid()}")

    blockchain.chain[1].transactions[1].amount = 20
    print("Modifying blockchain...")
    print(f"Blockchain validity: {blockchain.is_valid()}")

