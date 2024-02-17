from os import path
import json
from crypto.aes import AES
from utils.util import c2b, c2s, hash_msg


class FileHandler:
    def __init__(self, node):
        self.node = node
        self.files = {}

        self.load_files_info()


    def update_files_info(self, info, file_name, file_path):
        self.files[file_name] = {"info": info, "path": file_path}
        try:
            # store the file info in the file_info.json
            with open(path.join(self.node.working_dir, 'files_info.json'), 'w') as f:
                f.write(json.dumps(self.files))
            return True
        except Exception as e:
            print(e)
            return False

    def load_files_info(self):
        try:
            with open(path.join(self.node.working_dir, 'files_info.json'), 'r') as f:
                self.files = json.loads(f.read())
        except Exception as e:
            print(e)
            return {}


    def save_file(self, data: bytes, file_name: str, file_path: str):
        aes = AES()
        nonce, cipher = aes.encrypt(data)
        hash_cipher = hash_msg(cipher)
        signature = self.node.communicator.signer.sign_message(hash_cipher)

        try:
            with open(path.join(file_path, f"R_{file_name}.txt"), 'wb') as f:
                f.write(cipher)
                info = {
                    "aes_key": c2s(aes.key),
                    "nonce": c2s(nonce),
                    "hash": c2s(hash_cipher),
                    "signature": c2s(signature),
                    "size": len(cipher),
                    "owner": self.node.node_id
                }
                self.update_files_info(info, file_name, file_path)
            return True
        except Exception as e:
            print(e)
            return False

    def save_peer_file(self, cipher: bytes, info: dict, file_name: str, file_path: str):
        try:
            with open(path.join(file_path, f"R_{file_name}.txt"), 'wb') as f:
                # validate the signature
                f.write(cipher)
                self.update_files_info(info, file_name, file_path)

            return True
        except Exception as e:
            print(e)
            return False

    def read_file_info(self, file_name: str):
        try:
            return self.files[file_name]
        except Exception as e:
            print(e)
            return None

    def read_file(self, file_name: str, file_path: str):
        try:
            info = self.files[file_name]['info']
            aes_key = c2b(info['aes_key'])
            nonce = c2b(info['nonce'])
            aes = AES(aes_key, nonce)

            with open(path.join(file_path, file_name), 'rb') as d:
                data = aes.decrypt(d.read())
                if data is not None:
                    return data

        except Exception as e:
            print(e)
            return None, None




