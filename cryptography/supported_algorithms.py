import oqs
import hashlib

SUPPORTED_SIGNATURE_ALGORITHMS = [alg for alg in oqs.get_enabled_sig_mechanisms() if alg not in ['Falcon-padded-512', 'Falcon-padded-1024']]

SUPPORTED_HASH_FUNCTIONS = (hashlib.algorithms_guaranteed | {'shake_128_x', 'shake_256_x'}) - {'shake_128', 'shake_256'}