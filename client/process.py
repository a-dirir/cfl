from os import path, mkdir
from time import time
from utils.util import c2b, c2s, hash_msg
import json
from client.storage_controller import StorageController


class Process:
    def __init__(self, node, process_id, client_config: dict, callbacks: dict = None):
        self.node = node
        self.process_id = process_id
        self.callbacks = callbacks

        self.storage_controller = StorageController(self.node, client_config)

        self.process_config, self.participants = self.load_config()

    def load_config(self):
        process_info = self.node.registration.get_process(self.process_id)

        process_directory = path.join(self.node.working_dir, "Processes", f"Process_{self.process_id}")

        if not path.exists(process_directory):
            mkdir(process_directory)

        return process_info['config'], process_info['participants']

    def call_orchestrator(self, request_type: str, data: dict):
        msg = {
            "access": f"Process:Manager:{request_type}",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id,
                "data": data
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def run(self):
        pass





