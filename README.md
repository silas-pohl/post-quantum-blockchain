**1. Implement a minimal Blockchain in Python:**
- Creating wallets (generating key pairs)
- Creating transactions (singing and verifying)
- Mining pending transactions (creating hashes to add new blocks)
- Verifying the integrity of the blockchain (verifying hashes)
- Exchangeable `CryptoProvider` (initially classic cryptography, e.g. `ECDSA` and `SHA256`)

**2. Research about most promising Post-Quantum-Cryptography:**
- Hash-Based Signatures like `SPHINCS+` and `XMSS`
- Lattice-Based Cryptography like `CRYSTALS-Dilithium` and `FALCON`
- Multivariate Polynomial Cryptography like `Rainbow`

**3. Implement a selection of Post-Quantum-CryptoProviders for our Blockchain**

**4. Comparative analysis of the Blockchain with classic CryptoProvider and Post-Quantum-CryptoProviders:**
- Key Size and Signature Size
- Computational Efficiency (Transaction Creation Time, Mining/Validation Time)
- Memory and Storage Usage (Memory Usage, Blockchain Storage)

**5. Evaluation of the experimental results:**
-  Assessment of the feasibility of introducing today's post-quantum cryptography into blockchains (e.g. Bitcoin)
- Evaluation of the limitation of the experiment (e.g. performance impact of the use of python)

---
**Further work (probably out of scope):**
- Extend the Blockchain with networking capabilities to distribute it on different systems
- Repeat the comparative analysis and measurements (adding transactions, mining blocks, etc.) in a distributed environment to get information about Bandwidth Usage, Verification Time, Synchronization Time, Latency, etc.
