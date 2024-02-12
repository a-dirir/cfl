from utils.util import c2s



class Registration:
    def __init__(self, node, main_server):
        self.node = node
        self.main_server = main_server

    def create_node(self, info: dict = None):
        msg = {
            "access": "Registration:Node:createNode",
            "data": {
                "pek": c2s(self.node.communicator.encryptor.get_public_key()),
                "psk": c2s(self.node.communicator.signer.get_public_key()),
                "info": info
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def update_node(self, info: dict = None):
        if info is None:
            return None

        msg = {
            "access": "Registration:Node:updateNode",
            "data": {
                "node_id": f"{self.node.node_id}",
                "pek": c2s(self.node.communicator.encryptor.get_public_key()),
                "psk": c2s(self.node.communicator.signer.get_public_key()),
                "info": info
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def get_node(self, node_id: int):
        msg = {
            "access": "Registration:Node:getNode",
            "data": {
                "node_id": f"{node_id}"
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def get_nodes(self):
        msg = {
            "access": "Registration:Node:getNodes",
            "data": {}
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def delete_node(self):
        msg = {
            "access": "Registration:Node:deleteNode",
            "data": {
                "node_id": f"{self.node.node_id}"
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def create_process(self, config: dict = None):
        msg = {
            "access": "Registration:Process:createProcess",
            "data": {
                "config": config
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def get_process(self, process_id: int):
        msg = {
            "access": "Registration:Process:getProcess",
            "data": {
                "process_id": f"{process_id}"
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def get_processes(self):
        msg = {
            "access": "Registration:Process:getProcesses",
            "data": {}
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def update_process(self, process_id, config: dict = None):
        if config is None:
            return None

        msg = {
            "access": "Registration:Process:updateProcess",
            "data": {
                "process_id": f"{process_id}",
                "config": config
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def delete_process(self, process_id: int):
        msg = {
            "access": "Registration:Process:deleteProcess",
            "data": {
                "process_id": f"{process_id}"
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None

    def participate(self, process_id: int):
        msg = {
            "access": "Registration:Process:Participate",
            "data": {
                "process_id": f"{process_id}",
                "node_id": self.node.node_id,
            }
        }

        response = self.node.send_request(msg, self.node.main_server.ec_key, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None
