from utils.util import c2s


class Registration:
    def __init__(self, node):
        self.node = node

    def create_node(self, info: dict = None):
        msg = {
            "access": "Registration:Node:createNode",
            "data": {
                "pek": c2s(self.node.communicator.encryptor.get_public_key()),
                "psk": c2s(self.node.communicator.signer.get_public_key()),
                "info": info
            }
        }

        return self.call_main_server(msg)

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

        return self.call_main_server(msg)

    def get_node(self, node_id: int):
        msg = {
            "access": "Registration:Node:getNode",
            "data": {
                "node_id": f"{node_id}"
            }
        }

        return self.call_main_server(msg)

    def get_nodes(self):
        msg = {
            "access": "Registration:Node:getNodes",
            "data": {}
        }

        return self.call_main_server(msg)

    def delete_node(self):
        msg = {
            "access": "Registration:Node:deleteNode",
            "data": {
                "node_id": f"{self.node.node_id}"
            }
        }

        return self.call_main_server(msg)

    def create_process(self, config: dict = None):
        msg = {
            "access": "Registration:Process:createProcess",
            "data": {
                "config": config
            }
        }

        return self.call_main_server(msg)

    def get_process(self, process_id: int):
        msg = {
            "access": "Registration:Process:getProcess",
            "data": {
                "process_id": f"{process_id}"
            }
        }

        return self.call_main_server(msg)

    def get_processes(self):
        msg = {
            "access": "Registration:Process:getProcesses",
            "data": {}
        }

        return self.call_main_server(msg)

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

        return self.call_main_server(msg)

    def delete_process(self, process_id: int):
        msg = {
            "access": "Registration:Process:deleteProcess",
            "data": {
                "process_id": f"{process_id}"
            }
        }

        return self.call_main_server(msg)

    def participate(self, process_id: int, config: dict):
        msg = {
            "access": "Registration:Process:Participate",
            "data": {
                "process_id": f"{process_id}",
                "node_id": self.node.node_id,
                "config": config
            }
        }

        return self.call_main_server(msg)

    def call_main_server(self, msg: dict):
        response = self.node.send_request(msg, self.node.main_server.pek, self.node.main_server.url)
        if response is not None:
            return response
        else:
            return None
