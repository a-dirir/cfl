from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests
from utils.util import c2b


class MainServerInfo:
    def __init__(self, url: str):
        self.url = url
        self.psk = None
        self.pek = None

    def get_public_keys(self):
        response = requests.get(f"{self.url}/info")
        if response.status_code == 200:
            msg = response.json()['msg']

            self.psk = serialization.load_pem_public_key(c2b(msg['psk']), backend=default_backend()).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            self.pek = serialization.load_pem_public_key(c2b(msg['pek']), backend=default_backend()).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        else:
            return None
