import pickle
from os import urandom
from crypto.aes import AES
from crypto.ec_key_exchanger import ECKeyExchanger
from crypto.digital_signer import DigitalSigner
from utils.util import c2b, c2s



class CommunicationHandler:
    def __init__(self, node_id: int = -99, keys_directory: str = None, generate_keys: bool = False):
        self.node_id = node_id
        if not generate_keys:
            self.encryptor = ECKeyExchanger(directory_path=keys_directory)
            self.signer = DigitalSigner(directory_path=keys_directory)
        else:
            self.encryptor = ECKeyExchanger(generate_keys=True)
            self.signer = DigitalSigner(generate_keys=True)

        self.lookup = {}

    def outgress(self, msg: dict, peer_pek: bytes = None):
        msg = pickle.dumps(msg)
        shared_key = self.encryptor.get_shared_key(peer_pek)
        nonce = urandom(16)

        aes = AES(key=shared_key, nonce=nonce)
        _, msg_cipher = aes.encrypt(msg)
        signature = self.signer.sign_message(msg)

        if signature is None or msg_cipher is None:
            return None

        out_msg = {
            "node_id": self.node_id,
            "content": msg_cipher,
            "nonce": nonce,
            "signature": signature,
            "ek": self.encryptor.get_public_key(),
            "sk": self.signer.get_public_key()
        }

        for key, value in out_msg.items():
            if key != "node_id":
                out_msg[key] = c2s(value)

        return out_msg

    def ingress(self, msg: dict, return_response=False):
        for key, value in msg.items():
            if key != "node_id":
                msg[key] = c2b(value)

        pek = msg["ek"]

        shared_key = self.encryptor.get_shared_key(msg["ek"])
        nonce = msg["nonce"]

        aes = AES(shared_key, nonce)
        out_msg = aes.decrypt(msg["content"])

        signature_valid = self.signer.verify_other_signatures(msg["signature"], out_msg, msg["sk"])
        if out_msg is not None and signature_valid:
            if return_response:
                return [pickle.loads(out_msg), msg]
            else:
                return pickle.loads(out_msg)
        else:
            return None

