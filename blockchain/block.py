import cryptography
from typing import List
import time
from .transaction import Transaction

class Block:
    """
    Represents a block in a blockchain.

    Each block contains a list of transactions, a reference to the previous block's hash,
    and is associated with a cryptographic provider for hashing and verification. The block
    includes metadata such as a timestamp, a nonce for proof-of-work, and its own computed hash.
    """

    def __init__(self, index: int, previous_hash: str, transactions: List[Transaction], crypto_provider: cryptography.CryptoProvider, timestamp=None):
        """
        Initialize a new block.

        Args:
            index (int): The index of the block in the blockchain.
            previous_hash (str): The hash of the previous block in the chain.
            transactions (List[Transaction]): A list of transactions included in the block.
            crypto_provider (CryptoProvider): The cryptographic provider used for hashing and verification.
            timestamp (float, optional): The timestamp of block creation. Defaults to the current time.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.crypto_provider = crypto_provider
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = None

    def compute_hash(self) -> bytes:
        """
        Compute the cryptographic hash of the block's contents (block's index, previous hash, transactions, timestamp, and nonce)

        Returns:
            bytes: The computed hash of the block as a hexadecimal string.
        """
        block = f'{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}'.encode()
        return self.crypto_provider.hash(block)

    def is_valid(self) -> bool:
        """
        Verify the validity of the block. Checks that all transactions in the block are valid and that the block's hash matches
        the computed hash based on its current contents.

        Returns:
            bool: True if the block is valid; False otherwise.
        """
        print(self.hash)
        print(self.compute_hash())

        if (
            not all(transaction.is_valid() for transaction in self.transactions) or
            self.hash != self.compute_hash()
        ):
            return False
        return True

    def __str__(self) -> str: # pragma: no cover
        return (
                f"Block #{self.index}\n"
                f"Previous Hash: {self.previous_hash}\n"
                f"Transactions:" + "\n  | ".join(str(transaction) for transaction in self.transactions) + "\n"
                f"Timestamp: {self.timestamp}\n"
                f"Nonce: {self.nonce}\n"
                f"Hash: {self.hash}"
        )