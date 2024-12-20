import hashlib
import ecdsa
from typing import Tuple
import oqs

class CryptoProvider:
    def __init__(self, signature_algorithm, hashing_algorithm):
        self.signature_algorithm = signature_algorithm
        self.hashing_algorithm = hashing_algorithm

    def __repr__(self):
        return "CryptoProvider" + self.signature_algorithm + self.hashing_algorithm

    def generate_keypair(self) -> Tuple[bytes, bytes]:
        if self.signature_algorithm == 'ECDSA-SHA256':
            secret_key_obj = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
            public_key_obj = secret_key_obj.get_verifying_key()
            secret_key = secret_key_obj.to_der()
            public_key = public_key_obj.to_der()
        else:
            with oqs.Signature(self.signature_algorithm) as generator:
                public_key = generator.generate_keypair()
                secret_key = generator.export_secret_key()
        return public_key, secret_key

    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        if self.signature_algorithm == 'ECDSA-SHA256':
            signature = ecdsa.SigningKey.from_der(secret_key).sign(message)
        else:
            with oqs.Signature(self.signature_algorithm, secret_key) as signer:
                print(message)
                signature = signer.sign(message)
        return signature

    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        if self.signature_algorithm == 'ECDSA-SHA256':
            try:
                is_valid = ecdsa.VerifyingKey.from_der(public_key).verify(signature, message)
            except ecdsa.BadSignatureError:
                is_valid = False
        else:
            with oqs.Signature(self.signature_algorithm) as verifier:
                is_valid = verifier.verify(message, signature, public_key)
        return is_valid

    def hash(self, data: bytes) -> bytes:
        if self.hashing_algorithm.startswith('shake'):
            h = hashlib.new('_'.join(self.hashing_algorithm.split('_')[:2]))
            h.update(data)
            digest = h.digest(int(self.hashing_algorithm.split('_')[2]))
        else:
            h = hashlib.new(self.hashing_algorithm)
            h.update(data)
            digest = h.digest()
        return digest