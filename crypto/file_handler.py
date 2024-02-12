from os import path
import json
from crypto.aes import AES
from utils.util import c2b, c2s, hash_msg


class FileHandler:
    def __init__(self, node):
        self.node = node
        self.storage_directory = ''
        self.files = {}

    def set_directory(self, storage_directory):
        self.storage_directory = storage_directory
        self.load_files_info(self.storage_directory)

    def update_files_info(self, info, file_name, file_path):
        self.files[file_name] = info

        try:
            # store the file info in the file_info.json
            with open(path.join(file_path, 'files_info.json'), 'w') as f:
                f.write(json.dumps(self.files))
            return True
        except Exception as e:
            print(e)
            return False

    def load_files_info(self, file_path):
        if path.exists(path.join(file_path, 'files_info.json')):
            try:
                with open(path.join(file_path, 'files_info.json'), 'r') as f:
                    self.files = json.loads(f.read())
            except Exception as e:
                print(e)
                return {}
        else:
            return {}

    def save_file(self, data: bytes, file_name: str, file_path: str = None):
        if file_path is None:
            file_path = self.storage_directory

        aes = AES()
        nonce, cipher = aes.encrypt(data)
        hash_cipher = hash_msg(cipher)
        signature = self.node.communicator.signer.sign_message(hash_cipher)

        try:
            with open(path.join(file_path, file_name), 'wb') as f:
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

    def save_peer_file(self, cipher, info, file_name, file_path=None):
        if file_path is None:
            file_path = self.storage_directory

        try:
            with open(path.join(file_path, file_name), 'wb') as f:
                f.write(cipher)
                self.update_files_info(info, file_name, file_path)

            return True
        except Exception as e:
            print(e)
            return False

    def read_file(self, file_name: str, file_path: str = None, info_only: bool = False):
        if file_path is None:
            file_path = self.storage_directory

        try:
            info = self.files[file_name]
            if info_only:
                return info

            aes_key = c2b(info['aes_key'])
            nonce = c2b(info['nonce'])
            aes = AES(aes_key, nonce)
            with open(path.join(file_path, file_name), 'rb') as d:
                data = aes.decrypt(d.read())
                if data is not None:
                    return data, info
        except Exception as e:
            print(e)
            return None, None




