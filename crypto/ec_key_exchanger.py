from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from os import path, getcwd
from utils.util import c2s, c2b




class ECKeyExchanger:
    def __init__(self, generate_keys=False, directory_path=None):
        if generate_keys:
            self.private_key = X25519PrivateKey.generate()
            self.public_key = self.private_key.public_key()
        else:
            self.load_keys(directory_path)

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def store_keys(self, directory_path=getcwd()):
        private_key_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_str = c2s(private_key_bytes)
        with open(path.join(directory_path, "private_key_encryption.pem"), "w") as f:
            f.write(private_key_str)

        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_str = c2s(public_key_bytes)
        with open(path.join(directory_path, "public_key_encryption.pem"), "w") as f:
            f.write(public_key_str)

    def load_keys(self, directory_path=getcwd()):
        with open(path.join(directory_path, "private_key_encryption.pem"), "r") as f:
            private_key_bytes = c2b(f.read())
            self.private_key = serialization.load_pem_private_key(private_key_bytes,
                                                                  password=None,  backend=default_backend())

        with open(path.join(directory_path, "public_key_encryption.pem"), "r") as f:
            public_key_bytes = c2b(f.read())
            self.public_key = serialization.load_pem_public_key(public_key_bytes,  backend=default_backend())

    def get_shared_key(self, peer_public_key):
        try:
            peer_public_key = serialization.load_pem_public_key(peer_public_key,  backend=default_backend())
            shared_key = self.private_key.exchange(peer_public_key)
            derived_key = HKDF(algorithm=hashes.SHA256(), length=32,
                               salt=None, info=b"",  backend=default_backend()).derive(shared_key)
            return derived_key
        except Exception as e:
            return None

