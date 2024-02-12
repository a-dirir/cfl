from os import path, mkdir
from time import time
from utils.util import c2b, c2s, hash_msg
import json


class Process:
    def __init__(self, node, process_id: int, callback=None):
        self.node = node
        self.process_id = process_id
        self.callback = callback

        self.config, self.nodes = self.load_config()

        self.start = self.config['start']
        self.back_off_period = self.config['back_off_period']
        self.num_rounds = self.config['num_rounds']
        self.current_stage = ""

        self.tokens_generated = {}
        self.tokens_downloaded = {}
        self.resources_downloaded = {}
        self.computations_performed = {}
        self.jobs = {}

    def load_config(self):
        config = self.node.registration.get_process(self.process_id)
        process_directory = path.join(self.node.working_dir, "Processes", f"Process_{self.process_id}")

        if not path.exists(process_directory):
            mkdir(process_directory)

        self.node.file_handler.set_directory(process_directory)

        nodes = self.node.registration.get_nodes()

        return config, nodes

    def update_stage(self):
        current_time = time()

        s1 = self.start + self.config['t0'] + self.back_off_period
        s2 = s1 + self.config['t1'] + self.back_off_period
        s3 = s2 + self.config['t2'] + self.back_off_period
        s4 = s3 + self.config['t3'] + self.back_off_period

        if self.start < current_time < self.start + self.config['t0']:
            self.current_stage = "S0"
        elif s1 < current_time < s1 + self.config['t1']:
            self.current_stage = "S1"
        elif s2 < current_time < s2 + self.config['t2']:
            self.current_stage = "S2"
        elif s3 < current_time < s3 + self.config['t3']:
            self.current_stage = "S3"
        elif s4 < current_time < s4 + self.config['t4']:
            self.current_stage = "S4"
        elif s4 + self.config['t4'] < current_time:
            self.start = s4 + self.config['t4'] - self.back_off_period - self.config['t0']
            self.current_stage = "S1"

    def add_resources(self, resources: dict):
        # save resources locally
        for block_num, block in resources.items():
            for complement_idn, complement in block.items():
                complement_hash = hash_msg(complement)
                self.node.file_handler.save_file(complement, complement_hash)

        # send resources to scheduler
        msg = {
            "access": "Process:Manager:AddResources",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id,
                "resources": resources
            }
        }

        response = self.node.send_request(msg)
        if response is not None:
            return response
        else:
            return None

    def get_jobs(self):
        self.update_stage()

        if self.current_stage != "S1":
            # wait
            pass

        # get jobs from scheduler
        msg = {
            "access": "Process:Manager:GetJobs",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id
            }
        }

        response = self.node.send_request(msg)

        self.jobs = response

    def add_tokens(self, tokens: dict):
        # send tokens to scheduler
        msg = {
            "access": "Process:Manager:AddTokens",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id,
                "tokens": tokens
            }
        }

        response = self.node.send_request(msg)
        if response is not None:
            return response
        else:
            return None

    def get_tokens(self):
        # get tokens from scheduler
        msg = {
            "access": "Process:Manager:GetTokens",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id
            }
        }

        response = self.node.send_request(msg)
        if response is not None:
            return response
        else:
            return None

    def submit_jobs(self, results: dict):
        # send results to scheduler
        msg = {
            "access": "Process:Manager:SubmitJobs",
            "data": {
                "process_id": self.process_id,
                "node_id": self.node.node_id,
                "results": results
            }
        }

        response = self.node.send_request(msg)
        if response is not None:
            return response
        else:
            return None

    def perform_tokenization(self, tokens: dict):
        generated_tokens = {}
        for idn, non_holders in tokens.items():
            generated_tokens[idn] = {}
            info = self.node.file_handler.files[idn]
            for non_holder in non_holders.keys():

                # sign the message
                sender_psk = self.nodes[f"{non_holder}"]['psk']
                token = c2b(json.dumps(
                    {
                        "file_name": idn,
                        "sender": non_holder,
                        "sender_psk": sender_psk,
                        "process_id": self.process_id,
                        "info": info,
                    }))
                generated_tokens[idn][non_holder] = self.node.communicator.signer.sign(token)

        return generated_tokens
           
    def download_resources(self, resources: dict):
        for idn, resource in resources.items():
            holders = resource['holders']
            for holder in holders:
                token = self.tokens_downloaded[idn][holder]
                holder_pek = self.nodes[f"{holder}"]['pek']
                holder_psk = self.nodes[f"{holder}"]['psk']

                msg = {
                    "token": token,
                    "file_name": idn
                }

                holder_end_point = "find it"

                response = self.node.download_file(msg, holder_pek, holder_psk, idn, holder_end_point)
                if response is not None:
                    self.resources_downloaded[idn] = response
                    break
                else:
                    continue


    def perform_computation(self, jobs: dict):
        pass


