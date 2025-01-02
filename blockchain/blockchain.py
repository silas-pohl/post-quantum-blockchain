import cryptography
from .block import Block
from .transaction import Transaction

class Blockchain:
    """
    Represents a blockchain, which is a sequence of blocks containing transactions.

    The blockchain maintains a chain of blocks, manages pending transactions, and enables
    the mining process. It includes methods for validating the chain and retrieving balances
    for specific addresses.
    """

    def __init__(self, block_size: int, difficulty: int, crypto_provider: cryptography.CryptoProvider):
        """
        Initialize a new blockchain.

        Args:
            block_size (int): The maximum number of transactions per block.
            difficulty (int): The difficulty level for the proof-of-work algorithm, determining the number of leading zeros required in the hash.
            crypto_provider (CryptoProvider): The cryptographic provider used for hashing and verification.
        """
        self.block_size = block_size
        self.difficulty = difficulty
        self.crypto_provider = crypto_provider
        self.chain = []
        self.pending_transactions = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """
        Create the genesis (first) block in the blockchain. The genesis block has no previous hash, no transactions, and
        is precomputed with a valid hash. Should not be called manually.
        """
        genesis_block = Block(0, "0", [], self.crypto_provider)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction):
        """
        Add a new transaction to the list of pending transactions.

        Args:
            transaction (Transaction): The transaction to be added to the blockchain.
        """
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        """
        Mine the pending transactions and add a new block to the blockchain. Mines transactions up to the block size limit,
        computes the proof-of-work to meet the difficulty level, and adds the new block to the chain. Resets pending transactions
        after the block is mined.

        Returns:
            str: Message indicating if there were no transactions to mine.
        """
        if not self.pending_transactions:
            return "No transactions to mine."
        block = Block(len(self.chain), self.chain[-1].compute_hash(), self.pending_transactions[:self.block_size], self.crypto_provider)
        while not block.compute_hash().startswith(b'\x00' * self.difficulty):
            block.nonce += 1
        block.hash = block.compute_hash()
        self.chain.append(block)
        self.pending_transactions = self.pending_transactions[self.block_size:]

    def is_valid(self) -> bool:
        """
        Verify the integrity of the blockchain. Checks each block in the chain to ensure all blocks are valid and that the hashes
        link correctly to maintain the chain's integrity.

        Returns:
            bool: True if the blockchain is valid; False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if (
                not current_block.is_valid() or
                current_block.previous_hash != previous_block.hash
            ):
                return False
        return True

    def get_balance(self, address):
        """
        Calculate the balance for a given address. Iterates through the blockchain to sum up all transactions related to the specified
        address to determine the current balance.

        Args:
            address (str): The address to calculate the balance for.

        Returns:
            int: The balance of the specified address.
        """
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.recipient == address:
                    balance += transaction.amount
                if transaction.sender == address:
                    balance -= transaction.amount
        return balance

    def __str__(self) -> str: # pragma: no cover
        return (
            f"Blockchain with Blocksize {self.block_size} and Difficulty {self.difficulty}\n\n"
            + "\n\n".join(str(block) for block in self.chain) + "\n"
            + "\nPending Transactions:" + "\n  | ".join(str(transaction) for transaction in self.pending_transactions) + "\n"
        )