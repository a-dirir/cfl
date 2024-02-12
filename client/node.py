import json
import requests
from os import path, mkdir, getenv
from uuid import uuid4
from client.registration import Registration
from crypto.communication_handler import CommunicationHandler
from crypto.file_handler import FileHandler
from utils.util import c2b, hash_msg

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class MainServer:
    def __init__(self):
        self.url = getenv("CFL_API_Server_URL")

        signature_key_bytes = c2b(getenv("CFL_API_Server_PSK"))
        self.ds_key = serialization.load_pem_public_key(signature_key_bytes, backend=default_backend()).public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        encryption_key_bytes = c2b(getenv("CFL_API_Server_PEK"))
        self.ec_key = serialization.load_pem_public_key(encryption_key_bytes, backend=default_backend()).public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )


class Node:
    def __init__(self, node_id=None):
        self.main_server = MainServer()
        if node_id is not None:
            self.node_id = node_id
            self.working_dir = path.join(getenv("Work_Directory"), 'client', f'Node_{self.node_id}')
            self.communicator = CommunicationHandler(node_id, self.working_dir)
            self.registration = Registration(self, self.main_server)

        else:
            self.communicator = CommunicationHandler(-99, generate_keys=True)
            self.registration = Registration(self, self.main_server)
            response = self.registration.create_node({"name": uuid4().hex})
            if response is not None:
                self.node_id = response['node_id']
                self.communicator.node_id = self.node_id
                self.working_dir = path.join(getenv("Work_Directory"), 'client', f'Node_{self.node_id}')
                mkdir(self.working_dir)
                mkdir(path.join(self.working_dir, "Processes"))
                self.communicator.signer.store_keys(self.working_dir)
                self.communicator.encryptor.store_keys(self.working_dir)

        self.file_handler = FileHandler(self)

    def send_request(self, msg: dict, peer_pek: bytes = None, end_point: str = None, return_response=False):
        if peer_pek is None:
            peer_pek = self.main_server.ec_key

        if end_point is None:
            end_point = self.main_server.url

        try:
            msg = self.communicator.outgress(msg, peer_pek)
            response = requests.post(end_point, json=msg).json()

            if response['status_code'] == 200:
                response = self.communicator.ingress(response['msg'], return_response)
                return response
            else:
                return None
        except Exception as e:
            return None

    def download_file(self, msg: dict, peer_pek: bytes, peer_psk: bytes,
                      file_name: str, storage_dir: str = None, end_point: str = None):
        if end_point is None:
            end_point = self.main_server.url

        try:
            msg = self.communicator.outgress(msg, peer_pek)
            response = requests.post(end_point, json=msg)
            if response.status_code == 200:
                info_cipher = json.loads(response.headers['info'].replace("'", "\""))
                info = self.communicator.ingress(info_cipher)
                file_hash = hash_msg(response.content)
                is_valid = self.communicator.signer.verify_other_signatures(c2b(info['signature']), file_hash, peer_psk)
                if is_valid:
                    self.file_handler.save_peer_file(response.content, info, f"R_{file_name}", storage_dir)
                    return info
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None

