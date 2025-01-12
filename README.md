# Post-Quantum-Blockchain
<img width="1602" alt="image" src="https://github.com/user-attachments/assets/3489946c-51f8-4b2a-9159-2bd672e3ea45" />

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.icons8.com/?size=512&id=13441&format=png" height="60">
  </a>
  <a href="https://docs.pytest.org/en/stable/">
    <img src="https://docs.pytest.org/en/stable/_static/pytest1.png" height="60">
  </a>
  <a href="https://numpy.org/">
    <img src="https://numpy.org/images/logo.svg" height="60">
  </a>
  <a href="https://matplotlib.org/stable/">
    <img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_001_2_00x.png" height="60">
  </a>
  <a href="https://openquantumsafe.org/">
    <img style="border-radius: 10px" src="https://avatars.githubusercontent.com/u/20689385?s=200&v=4" height="60">
  </a>
  <a href="https://containers.dev/">
    <img style="border-radius: 10px" src="https://avatars.githubusercontent.com/u/102692984?s=200&v=4" height="60">
  </a>
</p>

---
**“It’s time to prepare for quantum threats.”**

\- Dr. Lily Chen (mathematician and NIST fellow) in ["The race is on for quantum-safe cryptography", 2021](https://www.theverge.com/22523067/nist-challenge-quantum-safe-cryptography-computer-lattice)

---

### Description
This project aims to explore the research question "How feasible is the integration of quantum-safe signature algorithms into blockchains?" by setting up a minimal self-implemented python-based blockchain, which can be initialized with ECDSA or every quantum-safe signature algorithm supported by OQS. The comparative analysis focused on the three NIST standardized quantum-safe signature algorithms CRYSTALS-Dilithium, FALCON and SPHINCS+ and how their usage in the blockchain influences the performance and other attributes compared to the baseline with ECDSA signatures. More information can be found in the [project introduction slides](https://github.com/silas-pohl/post-quantum-blockchain/blob/master/project_introduction.pdf).

### Getting Started
Since the Open Quantum Safe Project, which provides the quantum safe signature algorithms, requires the local installation of the underlying C implementation, we decided to set up a Dev Container. This allows us to specify the installation of all requirements once in a Dockerfile, enabling easy use of this project without the requirement to install anything locally other than a Dev Container capable editor (rec. [Visual Studio Code](https://code.visualstudio.com/) + [Dev Container Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)) and [Docker](https://www.docker.com/).

1. Clone repository
```
git clone https://github.com/silas-pohl/post-quantum-blockchain
```
2. Open the Dev Container capable editor and open the repository folder as a Dev Container
3. If virtual environment (venv) not automatically activated:
```
source ../venv/bin/activate
```

### Running the Functional Test Suite
The following command will run the whole funtional test suite consisting of 358 tests to verify that every functionality of the blockchain works with every available signature algorithm (43) and hash function (14):
```
coverage run -m pytest tests/
```
To show the coverage report run:
```
coverage report
```
The current implementation has a functional test coverage of 100%.
```
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
blockchain/__init__.py                           3      0   100%
blockchain/block.py                             22      0   100%
blockchain/blockchain.py                        42      0   100%
blockchain/transaction.py                       15      0   100%
cryptography/__init__.py                         2      0   100%
cryptography/crypto_provider.py                 42      0   100%
cryptography/supported_algorithms.py             4      0   100%
tests/blockchain/test_block.py                  42      0   100%
tests/blockchain/test_blockchain.py             43      0   100%
tests/blockchain/test_transaction.py            33      0   100%
tests/cryptography/test_crypto_provider.py      33      0   100%
----------------------------------------------------------------
TOTAL                                          281      0   100%
```

### Running the Measurements
Prerequisites: Before running the script, ensure packages in requirements.txt are installed.

```
pip install -r requirements.txt
```

To run measurements and collect metrics on a selection of the supported signatures, run the script `performance_tests.py` inside `measurements` folder.
```
cd measurements
python performance_tests.py
```
The script will execute the following steps:

- Key and Signature Size Tests: Measures public key, private key, and signature sizes for supported algorithms.
- Transaction Efficiency Tests: Evaluates transaction creation, signature verification, and mining times (repeated and averaged over trials).
- Storage Usage Test: Measures the size of the blockchain after adding transactions and mining (repeated and averaged over trials).

The script automatically saves bar graphs showing the test results in a `figures/` folder as PNG files. If this folder does not exist, it will be created. These include:

- Public Key Size
- Private Key Size
- Signature Size
- Transaction Time
- Verification Time
- Mining Time
- Blockchain Storage Usage

The script currently tests and compares the following digital signature algorithms: ECDSA-SHA256, Falcon-512, Falcon-1024, Dilithium2, Dilithium3, Dilithium5, SPHINCS+-SHA2-256f-simple, SPHINCS+-SHA2-256s-simple. To add or modify algorithms, update the `self.algorithms` list in the `BlockchainTestSuite` class and ensure the `CryptoProvider` implementation supports the new algorithms.

You can adjust the test parameters by modifying the BlockchainTestSuite initialization in the `__main__` block:

```python
test_suite = BlockchainTestSuite(
    repeat_count=100,  # Number of repetitions for each test
    block_size=2,      # Number of transactions per block
    difficulty=1,      # Mining difficulty level
    hash_algorithm='sha512'  # Hashing algorithm used
)
```

For more customization, edit the respective test functions (`test_key_and_signature_sizes`, `test_transaction_efficiency`, `test_memory_and_storage`) in the script.

### Sample Usage of the Blockchain
To use the blockchain and implement own scenarios, the cryptography provider and the blockchain code can easily be imported into other python files.
```python
import cryptography
from blockchain import Transaction, Blockchain
import base64 #needed to use the public key as the public address
```

To create the "wallets" we us as part of our blockchain, we need to generate public keys and their corresponding secret keys. The used <signature_algorithm> and <hash_function> can be choosen freely out of all supported signature algorithms and hash functions (BUT: the same crypto provider should be used for key generation and all other blockchain operations). The constants `cryptography.SUPPORTED_SIGNATURE_ALGOROITHMS` and `cryptography.SUPPORTED_HASH_FUNCTIONS` contain the respective lists.
```python
crypto_provider = cryptography.CryptoProvider(<signature_algorithm>, <hash_function>)
public_key1, secret_key1 = crypto_provider.generate_keypair()
address1 = base64.b64encode(public_key1).decode("utf-8")
public_key2, secret_key2 = crypto_provider.generate_keypair()
address2 = base64.b64encode(public_key2).decode("utf-8")
```

The next step would be to create some sample transactions that we want to add to the blockchain.
```python
transaction1 = Transaction(address1, address2, 30, crypto_provider)
transaction1.sign_transaction(secret_key1)
transaction2 = Transaction(address2, address1, 10, crypto_provider)
transaction2.sign_transaction(secret_key2)
transaction3 = Transaction(address2, address1, 15, crypto_provider)
transaction3.sign_transaction(secret_key2)
```
Lastly, we can initiate our blockchain and add our transactions to it. We can choose the `<block_size>` (how many transactions should fit into one block) and the `<difficulty>` (the quantity of leading 0s for a block hash to be valid) when initiating the blockchain.
```python
blockchain = Blockchain(<block_size>, <difficulty>, crypto_provider)
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)
```
Now we have a simple blockchain containing three unmined transactions. We can now start the mining process to try to find a valid hash for the first block containing transactions.
```python
blockchain.mine_pending_transactions()
```
This process takes time depending on the choosen `<difficulty>` and once done, the first `<block_size>` amount of transaction will be mined. If the choosen `<block_size>` in this example is 3 or more, all added transactions will be mined and the funds of address1 will be -5 and of address2 will be 5.
```python
blockchain.get_balance(address1)
blockchain.get_balance(address2)
```
The integrity of the blockchain (Each block in the chain is valid and all hashes link correctly) can be verified.
```python
blockchain.is_valid()
```
Further information about the functionality of each component of the blockchain can be read in the extensive Docstrings of each method and class in the source code.
