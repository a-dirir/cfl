from time import time
from process.scheduling.scheduler import Scheduler


class Process:
    def __init__(self, config: dict, nodes: list):
        self.config = config
        self.start = config['start']
        self.back_off_period = config['back_off_period']
        self.num_rounds = config['num_rounds']
        self.current_stage = ""

        self.nodes = nodes

        self.resources = {}

        self.scheduler = None

        self.update_stage()

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

        if self.scheduler is not None and self.scheduler.is_round_complete():
            if self.num_rounds > 0:
                self.num_rounds -= 1
                self.current_stage = "S0"
                self.scheduler = None

    def add_resources(self, node_id: int, resources: dict):
        self.update_stage()

        if self.current_stage != "S0":
            return {'error': 'Process not in S0 stage'}, 400

        if node_id in self.nodes:
            self.resources[node_id] = resources

            return {}, 200

        return {'error': 'Node not in Process'}, 400

    def get_jobs(self, node_id: int):
        self.update_stage()

        if self.current_stage != "S1":
            return {'error': 'Process not in S1 stage'}, 400

        if self.scheduler is None:
            self.scheduler = Scheduler(self.resources, self.config)
            self.scheduler.compute()

        if node_id in self.nodes:
            return self.scheduler.get_jobs(node_id), 200

        return {'error': 'Node not in Process'}, 400

    def add_tokens(self, node_id: int, tokens: dict):
        self.update_stage()

        if self.current_stage != "S2":
            return {'error': 'Process not in S2 stage'}, 400

        if node_id in self.nodes:
            self.scheduler.add_tokens(node_id, tokens)

            return {}, 200

        return {'error': 'Node not in Process'}, 400

    def get_tokens(self, node_id: int):
        self.update_stage()

        if self.current_stage != "S3":
            return {'error': 'Process not in S3 stage'}, 400

        if node_id in self.nodes:
            return self.scheduler.get_tokens(node_id), 200

        return {'error': 'Node not in Process'}, 400

    def submit_jobs(self, node_id: int, results: dict):
        self.update_stage()

        if self.current_stage != "S4":
            return {'error': 'Process not in S4 stage'}, 400

        if node_id in self.nodes:
            self.scheduler.submit_jobs(node_id, results)

            return {}, 200

        return {'error': 'Node not in Process'}, 400
