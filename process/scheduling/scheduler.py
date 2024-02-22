from process.policies.consensus.default_consensus_algorithm import DefaultConsensusAlgorithm
from process.policies.grouping.default_grouping_algorithm import DefaultGroupingAlgorithm
from process.scheduling.mapping_tables import MappingTables
from process.state.state import State
from process.scheduling.jobs import Jobs


class Scheduler:
    def __init__(self, workers: list, config: dict):
        self.workers = workers
        self.config = config

        self.groups = DefaultGroupingAlgorithm(self.workers, config).apply()

        self.mapping_tables = MappingTables(self.groups, config)

        self.consensus_algorithm = DefaultConsensusAlgorithm(config)

        self.state = State(self, self.groups, config)

        self.jobs = Jobs(self.workers)

        self.tokens = {worker_id: {} for worker_id in self.workers}

    def schedule(self, tree_node):
        if tree_node.type == 'computation':
            self.schedule_computation(tree_node)
        elif tree_node.type == 'group':
            self.schedule_group(tree_node)

    def schedule_computation(self, tree_node):
        value, num_new_workers = self.consensus_algorithm.apply(tree_node)

        workers = self.mapping_tables.get_next_workers(tree_node, num_new_workers)

        tree_node.add_workers(workers)

        tree_node.value = value

        self.jobs.assign_jobs(tree_node, workers)

    def schedule_group(self, tree_node):
        if tree_node.check_commit():
            return

        self.jobs.assign_jobs(tree_node, tree_node.workers)

    def compute(self):
        self.state.root.compute()
        self.jobs.refresh()

    def get_jobs(self, worker_id: int):
        return self.jobs.get_jobs(worker_id)

    def add_tokens(self, worker_id: int, tokens: dict):
        for idn, token_values in tokens.items():
            for non_holder_worker, token in token_values.items():
                if self.jobs.check_upload_job_validity(worker_id, idn, non_holder_worker):
                    if self.tokens[non_holder_worker].get(idn) is None:
                        self.tokens[non_holder_worker][idn] = {}

                    self.tokens[non_holder_worker][idn][worker_id] = token

    def get_tokens(self, worker_id: int):
        return self.tokens[worker_id]

    def submit_jobs(self, worker_id: int, results: dict):
        for idn, result in results.items():
            if self.jobs.check_non_upload_job_validity(worker_id, result['type'], idn):
                self.state.add_results(worker_id, idn, result['value'])

    def is_round_complete(self):
        if self.state.root.check_commit():
            return True

        return False
