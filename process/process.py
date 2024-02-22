from time import time
from process.scheduling.scheduler import Scheduler


class Process:
    def __init__(self, workers: list, config: dict):
        self.workers = workers
        self.config = config

        self.scheduler = Scheduler(self.workers, self.config)

    def get_jobs(self, worker_id: int):
        if worker_id in self.workers:
            return self.scheduler.get_jobs(worker_id), 200

        return {'error': 'Error in getting jobs'}, 400

    def add_tokens(self, worker_id: int, tokens: dict):
        if worker_id in self.workers:
            self.scheduler.add_tokens(worker_id, tokens)

            return {}, 200

        return {'error': 'Error in adding tokens'}, 400

    def get_tokens(self, worker_id: int):
        if worker_id in self.workers:
            return self.scheduler.get_tokens(worker_id), 200

        return {'error': 'Error in getting tokens'}, 400

    def submit_jobs(self, worker_id: int, results: dict):
        if worker_id in self.workers:
            self.scheduler.submit_jobs(worker_id, results)

            return {}, 200

        return {'error': 'Error in submitting jobs'}, 400
