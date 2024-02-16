import requests
from os import path
import pickle
from storage.aws_s3 import AWSS3



class StorageController:
    def __init__(self, node, config: dict):
        self.node = node
        self.config = config
        self.nodes = config['nodes']
        self.file_extension = config['file_extension']

        self.controller = self.load_controller(config)

    @staticmethod
    def load_controller(config: dict):
        if config['storage_controller']['type'] == 'local':
            return None

        elif config['storage_controller']['type'] == 'aws':
            return AWSS3(config['storage_controller'])

    def upload(self, resources: dict):
        # always upload resources to the local directory (cache)
        for idn, data in resources.items():
            self.node.file_handler.save_file(data, idn, self.config['local_dir_path'])

            if self.controller is not None:
                # if a controller is loaded, upload the resources to the controller
                self.controller.upload(idn)

    def generate_token(self, resource_idn: str, non_holders: list):
        tokens = {}
        resource_info = self.node.file_handler.files[resource_idn]['info']

        if self.controller is not None:
            signed_url = self.controller.get_signed_url(resource_idn)
        else:
            signed_url = None

        for non_holder in non_holders:
            access = {'requester_id': non_holder, 'resource_idn': resource_idn,
                      'url': signed_url, 'info': resource_info}

            signature = self.node.communicator.signer.sign_message(pickle.dumps(access))

            tokens[non_holder] = self.node.communicator.outgress({'access': access, 'signature': signature},
                                                                 self.nodes[non_holder]['pek'])

        return tokens

    def download(self, resource_idn: str, holders: dict):
        for holder, encrypted_token in holders.items():
            token = self.node.communicator.ingress(encrypted_token)
            info = token['access']['info']
            signed_url = token['access']['url']

            if signed_url is not None:
                response = self.download_from_cloud_storage(resource_idn, signed_url, info)
            else:
                response = self.download_from_file_server(resource_idn, info, {'token': token}, holder)

            if response:
                return response

        return False

    def download_from_cloud_storage(self, resource_idn: str, signed_url: str, info: dict):
        response = requests.get(signed_url)
        if response.status_code == 200:
            self.node.file_handler.save_peer_file(response.content, info, resource_idn, self.config['local_dir_path'])
            return True
        else:
            return False

    def download_from_file_server(self, resource_idn: str, info: dict, msg: dict, holder: int):
        endpoint = self.nodes[holder]['storage']['endpoint']
        holder_pek = self.nodes[holder]['pek']

        msg = self.node.communicator.outgress(msg, holder_pek)
        response = requests.post(endpoint, json=msg)
        if response.status_code == 200:
            self.node.file_handler.save_peer_file(response.content, info, resource_idn, self.config['local_dir_path'])
            return True
        else:
            return False


