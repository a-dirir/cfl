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
        self.registration = Registration(self, self.main_server)

        if node_id is not None:
            self.node_id = node_id
            self.working_dir = path.join(getenv("Work_Directory"), 'client', f'Node_{self.node_id}')
            self.communicator = CommunicationHandler(node_id, self.working_dir)
        else:
            self.create_node()


        self.file_handler = FileHandler(self)

    def create_node(self):
        self.communicator = CommunicationHandler(-99, generate_keys=True)
        response = self.registration.create_node({"name": uuid4().hex})
        if response is not None:
            self.node_id = response['node_id']
            self.communicator.node_id = self.node_id

            self.working_dir = path.join(getenv("Work_Directory"), 'client', f'Node_{self.node_id}')
            mkdir(self.working_dir)
            mkdir(path.join(self.working_dir, "Processes"))

            self.communicator.signer.store_keys(self.working_dir)
            self.communicator.encryptor.store_keys(self.working_dir)

            # store the file info in the file_info.json
            with open(path.join(self.working_dir, 'files_info.json'), 'w') as f:
                f.write(json.dumps({}))



    def send_request(self, msg: dict, peer_pek: bytes = None, endpoint: str = None, return_response=False):
        if peer_pek is None:
            peer_pek = self.main_server.ec_key

        if endpoint is None:
            endpoint = self.main_server.url

        try:
            msg = self.communicator.outgress(msg, peer_pek)
            response = requests.post(endpoint, json=msg).json()

            if response['status_code'] == 200:
                response = self.communicator.ingress(response['msg'], return_response)
                return response
            else:
                return None
        except Exception as e:
            return None

