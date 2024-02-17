from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom


class AES:
    def __init__(self, key=None, nonce=None):
        self.aad = b'This is a decentralized Federated Learning System'

        if key is None:
            self.key = AESGCM.generate_key(bit_length=256)
        else:
            self.key = key

        if nonce is None:
            self.nonce = urandom(16)
        else:
            self.nonce = nonce

        self.aes = AESGCM(self.key)

    def encrypt(self, msg_bytes):
        try:
            msg_encrypted = self.aes.encrypt(self.nonce, msg_bytes, self.aad)
            return self.nonce, msg_encrypted
        except:
            return None, None

    def decrypt(self, cipher_text):
        try:
            return self.aes.decrypt(self.nonce, cipher_text, self.aad)
        except:
            return None
