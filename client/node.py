import json
import requests
from os import path, mkdir
from uuid import uuid4
from client.registration import Registration
from client.main_server_info import MainServerInfo
from crypto.communication_handler import CommunicationHandler
from crypto.file_handler import FileHandler


class Node:
    def __init__(self, node_id=None, root_dir: str = "",
                 main_server_url: str = "http://127.0.0.1:8080"):
        self.main_server = MainServerInfo(url=main_server_url)
        self.registration = Registration(self)

        if node_id is not None:
            self.node_id = node_id
            self.working_dir = path.join(root_dir, 'Clients', f'Node_{self.node_id}')
            self.communicator = CommunicationHandler(node_id, self.working_dir)
            self.file_handler = FileHandler(self)
        else:
            self.create_node(root_dir)



    def create_node(self, root_dir: str):
        self.communicator = CommunicationHandler(-99, generate_keys=True)
        response = self.registration.create_node({"name": uuid4().hex})
        if response is not None:
            self.node_id = response['node_id']
            self.communicator.node_id = self.node_id

            # check if the working directory/Clients exists
            if not path.exists(path.join(root_dir, 'Clients')):
                mkdir(path.join(root_dir, 'Clients'))

            self.working_dir = path.join(root_dir, 'Clients', f'Node_{self.node_id}')
            mkdir(self.working_dir)
            mkdir(path.join(self.working_dir, "Processes"))

            self.communicator.signer.store_keys(self.working_dir)
            self.communicator.encryptor.store_keys(self.working_dir)

            # store the file info in the file_info.json
            with open(path.join(self.working_dir, 'files_info.json'), 'w') as f:
                f.write(json.dumps({}))

            self.file_handler = FileHandler(self)

            return True
        else:
            return False

    def send_request(self, msg: dict, peer_pek: bytes = None, endpoint: str = None, return_response=False):
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
