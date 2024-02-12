import pickle
from client.node import Node


class LocalClient:
    def __init__(self, node: Node, file_extension: str = "txt"):
        self.node = node
        self.file_extension = file_extension

    def generate_token(self, resource_idn: str, non_holders: list):
        tokens = {}
        for non_holder in non_holders:
            access = {
                'requester_id': non_holder,
                'resource_idn': resource_idn,
            }

            signature = self.node.communicator.signer.sign_message(pickle.dumps(access))

            tokens[non_holder] = {
                'access': access,
                'signature': signature
            }

        return tokens

    def upload(self, resources: dict, config: dict = None):
        storage_dir = config['storage_dir']
        for idn, data in resources.items():
            self.node.file_handler.save_file(data, f"R_{idn}.{self.file_extension}", storage_dir)

    def download(self, resource_idn: str, holders: dict, config: dict = None):
        participants = config['participants']

        for holder, token in holders.items():
            peer_psk = participants[holder]['psk']
            peer_pek = participants[holder]['pek']
            endpoint = participants[holder]['storage']['end_point']

            msg = {
                'token': token
            }

            response = self.node.download_file(msg, peer_pek, peer_psk, f"{resource_idn}",
                                               config['storage_dir'], endpoint)

            if response is not None:
                return response


