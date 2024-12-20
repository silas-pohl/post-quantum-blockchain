import cryptography
import base64

class Transaction:
    """
    Represents a blockchain transaction between a sender and a recipient.

    This class contains the details of a transaction, including the sender, recipient,
    amount, and a cryptographic provider for signing and verifying the transaction.
    """

    def __init__(self, sender: str, recipient: str, amount: int, crypto_provider: cryptography.CryptoProvider):
        """
        Initialize a new transaction.

        Args:
            sender (str): The sender's public key as a base64-encoded string.
            recipient (str): The recipient's public key as a base64-encoded string.
            amount (int): The amount of funds to transfer.
            crypto_provider (CryptoProvider): The cryptographic provider used for signing and verifying the transaction.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.crypto_provider = crypto_provider
        self.signature = None

    def sign_transaction(self, private_key: bytes):
        """
        Sign the transaction using the sender's private key.

        Args:
            private_key (bytes): The sender's private key in bytes format.
        """
        transaction = f'{self.sender}{self.recipient}{self.amount}'.encode()
        print(f"Transaction to sign: {transaction}")
        print("\n")
        self.signature = self.crypto_provider.sign(private_key, transaction)

    def is_valid(self) -> bool:
        """
        Verify the validity of the transaction signature.

        Returns:
            bool: True if the transaction signature is valid; False otherwise.
        """
        transaction = f'{self.sender}{self.recipient}{self.amount}'.encode()
        return self.crypto_provider.verify(base64.b64decode(self.sender), transaction, self.signature)

    def __str__(self) -> str:
        return (
            "\n"
            f"  | Sender:     {self.sender}\n"
            f"  | Recipient:  {self.recipient}\n"
            f"  | Amount:     {self.amount}\n"
            f"  | Signature:  {base64.b64encode(self.signature).decode('utf-8')}"
        )