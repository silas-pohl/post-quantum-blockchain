<style>
.rounded {
    border-radius: 10px;
}
</style>

# Post-Quantum-Blockchain
<p align="center">
  <a href="https://www.python.org/">
    <img class="rounded" src="https://img.icons8.com/?size=512&id=13441&format=png" height="60">
  </a>
  <a href="https://docs.pytest.org/en/stable/">
    <img class="rounded" src="https://docs.pytest.org/en/stable/_static/pytest1.png" height="60">
  </a>
  <a href="https://numpy.org/">
    <img class="rounded" src="https://numpy.org/images/logo.svg" height="60">
  </a>
  <a href="https://matplotlib.org/stable/">
    <img class="rounded" src="https://matplotlib.org/stable/_images/sphx_glr_logos2_001_2_00x.png" height="60">
  </a>
  <a href="https://openquantumsafe.org/">
    <img class="rounded" src="https://avatars.githubusercontent.com/u/20689385?s=200&v=4" height="60">
  </a>
  <a href="https://containers.dev/">
    <img class="rounded" src="https://avatars.githubusercontent.com/u/102692984?s=200&v=4" height="60">
  </a>
</p>

## Evaluating the feasibility of introducing Post-Quantum-Cryptography in blockchains using the example of a minimal Python-based blockchain 

### Description
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
The current implementation has a functional test coverage of 100%
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

### Implement Own Scenarios
To implement own scenarios to eperiment with the blockchain, the cryptography provider and the blockchain code can easily imported into other python files.
```
import cryptography
from blockchain import Transaction, Blockchain
import base64 #needed to use the public key as the public address
``` 

The basic setup consists of two public addresses and their corresponding secret keys. <signature_algorithm> and <hash_function> can be choosen freely out of all supported signature algorithms and hash functions. The constants `cryptography.SUPPORTED_SIGNATURE_ALGOROITHMS` and `cryptography.SUPPORTED_HASH_FUNCTIONS` contain the respective lists.
```
crypto_provider = cryptography.CryptoProvider(<signature_algorithm>, <hash_function>)
public_key1, secret_key1 = crypto_provider.generate_keypair()
address1 = base64.b64encode(public_key1).decode("utf-8")
public_key2, secret_key2 = crypto_provider.generate_keypair()
address2 = base64.b64encode(public_key2).decode("utf-8")
```

The next step would be to create some sample transactions that we want to add to the blockchain.
```
transaction1 = Transaction(address1, address2, 30, crypto_provider)
transaction1.sign_transaction(secret_key1)
transaction2 = Transaction(address2, address1, 10, crypto_provider)
transaction2.sign_transaction(secret_key2)
transaction3 = Transaction(address2, address1, 15, crypto_provider)
transaction3.sign_transaction(secret_key2)
```
Lastly, we can initiate our blockchain and add our transactions to it. We can choose the <block_size> (how many transactions should fit into one block) and the <difficulty> (the quantity of leading 0s for a block hash to be valid) when initiating the blockchain.
```
blockchain = Blockchain(<block_size>, <difficulty>, crypto_provider)
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)
```
Now we have a simple blockchain containing three unmined transactions. We can now start the mining process to try to find the first non-genesis block.
```
blockchain.mine_pending_transactions()
```
This process takes time depending on the choosen <difficulty> and once done, the first <block_size> amount of transaction will be mined. If the choosen <block_size> in this example is 3 or more, all added transactions will be mined and the funds of address1 will be -5 and of address2 will be 5. This can be confirmed with:
```
blockchain.get_balance(address1)
blockchain.get_balance(address2)
```
To verify the integrity of the blockchain (checking that each block in the chain is valid and that the hashes link correctly) run the following:
```
blockchain.is_valid()
```