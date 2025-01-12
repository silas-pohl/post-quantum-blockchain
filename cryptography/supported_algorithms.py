import oqs
import hashlib

SUPPORTED_SIGNATURE_ALGORITHMS = (set(oqs.get_enabled_sig_mechanisms()) | {'ECDSA-SHA256'}) - {'Falcon-padded-512', 'Falcon-padded-1024'}
SUPPORTED_HASH_FUNCTIONS = (hashlib.algorithms_guaranteed | {'shake_128_x', 'shake_256_x'}) - {'shake_128', 'shake_256'}