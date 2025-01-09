import numpy as np
import matplotlib.pyplot as plt
import time
import os
from pympler import asizeof
import base64
import sys
sys.path.append('../')

from blockchain import Blockchain, Transaction
from cryptography import CryptoProvider

# Test Suite
class BlockchainTestSuite:
    def __init__(self, repeat_count=10, block_size=2, difficulty=1):
        self.algorithms = algorithms = ['ECDSA-SHA256', 'Falcon-512', 'Falcon-1024', 'Dilithium2', 'Dilithium3', 'Dilithium5', 'SPHINCS+-SHA2-256f-simple', 'SPHINCS+-SHA2-256s-simple']
        self.results = {
            "public_key_size": {},
            "private_key_size": {},
            "signature_size": {},
            "transaction_time": {},
            "verification_time": {},
            "mining_time": {},
            "storage_usage": {}
        }
        self.repeat_count = repeat_count
        self.block_size = block_size
        self.difficulty = difficulty

        self.providers = {}
        for algorithm in self.algorithms:
            provider = CryptoProvider(algorithm,'sha512')
            self.providers[algorithm] = provider

    def test_key_and_signature_sizes(self):
        for name, provider in self.providers.items():
            # Measure public and private key sizes
            public_key, private_key  = provider.generate_keypair()
            # Measure signature size
            message = "Test Message".encode()
            signature = provider.sign(private_key, message)

            self.results["public_key_size"][name] = len(public_key)
            self.results["private_key_size"][name] = len(private_key)
            self.results["signature_size"][name] = len(signature)

    def test_transaction_efficiency(self):
        for name, provider in self.providers.items():
            transaction_times = []
            verification_times = []
            mining_times = []

            for _ in range(self.repeat_count):
                blockchain = Blockchain(self.block_size, self.difficulty, provider)
                public_key1, private_key1  = provider.generate_keypair()
                sender = base64.b64encode(public_key1).decode("utf-8")
                public_key2, private_key2  = provider.generate_keypair()
                recipient = base64.b64encode(public_key2).decode("utf-8")

                # Measure transaction time
                start = time.time()
                tx = Transaction(sender, recipient, 10, provider)
                tx.sign_transaction(private_key1)
                transaction_times.append(time.time() - start)

                # Measure verification time
                start = time.time()
                tx.is_valid()
                verification_times.append(time.time() - start)

                blockchain.add_transaction(tx)

                # Measure mining time
                start = time.time()
                blockchain.mine_pending_transactions()
                mining_times.append(time.time() - start)

            # Take the mean and convert to milliseconds 
            self.results["transaction_time"][name] = np.mean(transaction_times) * 1000
            self.results["verification_time"][name] = np.mean(verification_times) * 1000
            self.results["mining_time"][name] = np.mean(mining_times) * 1000 

    def test_memory_and_storage(self, num_transactions=10):
        for name, provider in self.providers.items():
            storage_usages = []

            for _ in range(self.repeat_count):
                blockchain = Blockchain(self.block_size, self.difficulty, provider)
                public_key1, private_key1  = provider.generate_keypair()
                sender = base64.b64encode(public_key1).decode("utf-8")
                public_key2, private_key2  = provider.generate_keypair()
                recipient = base64.b64encode(public_key2).decode("utf-8")

                # Add transactions 
                for _ in range(num_transactions):
                    tx = Transaction(sender, recipient, 10, provider)
                    tx.sign_transaction(private_key1)
                    blockchain.add_transaction(tx)

                blockchain.mine_pending_transactions()

                # storage_size = sum(len(str(block).encode()) for block in blockchain.chain)
                storage_size = asizeof.asizeof(blockchain)
                storage_usages.append(storage_size)

            self.results["storage_usage"][name] = np.mean(storage_usages)

    def run_tests(self):
        print("Running Key and Signature Size Tests...")
        self.test_key_and_signature_sizes()
        print("Running Transaction Efficiency Tests...")
        self.test_transaction_efficiency()
        print("Running Memory and Storage Usage Tests...")
        self.test_memory_and_storage()
        self.display_results()

    def display_results(self):
        self.plot_results("Public Key Size", self.results["public_key_size"], "public_key_size", "Size (bytes)")
        self.plot_results("Private Key Size", self.results["private_key_size"], "private_key_size", "Size (bytes)")
        self.plot_results("Signature Size", self.results["signature_size"], "signature_size", "Size (bytes)")
        self.plot_results("Transaction Time", self.results["transaction_time"], "transaction_time", "Time (ms)")
        self.plot_results("Verification Time", self.results["verification_time"], "verification_time", "Time (ms)")
        self.plot_results("Mining Time", self.results["mining_time"], "mining_time", "Time (ms)")
        self.plot_results("Blockchain Storage Usage", self.results["storage_usage"], "storage_usage", "Bytes")

    def plot_results(self, title, data, label, ylabel):
        x = list(data.keys())
        values = list(data.values())

        plt.figure()
        bars = plt.bar(x, values)  # Store the bar objects
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xticks(rotation=60)
        plt.grid(axis='y')

        # Add values on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom')


        # Adjust y-axis limits to add some space above the tallest bar
        plt.ylim(0, max(values) * 1.1)  # Add 10% space above the tallest bar

        plt.tight_layout()

        # Create "figures" folder if it doesn't exist
        if not os.path.exists("figures"):
            os.makedirs("figures")

        # Save the figure 
        plt.savefig(os.path.join("figures", f"{label}.png"))

        plt.show()

if __name__ == "__main__":
    test_suite = BlockchainTestSuite()
    test_suite.run_tests()