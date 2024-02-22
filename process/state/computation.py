import pickle
from hashlib import sha256


class Computation:
    def __init__(self, block_num: int, group_index: int, children: list, scheduler, idn: str = None):
        self.type = "computation"
        self.idn = idn
        self.value = None

        self.block_num = block_num
        self.group_index = group_index
        self.children = children
        self.scheduler = scheduler

        self.results = {}
        self.workers = []
        self.computable = False

        self.set_identifier()

    def set_identifier(self):
        if self.idn is not None:
            return

        # get idns of children, sort them, convert to binary using pickle, hash the sorted list
        idns = [child.idn for child in self.children]
        idns.sort()
        idns = pickle.dumps(idns)
        self.idn = sha256(idns).hexdigest()

    def add_result(self, worker_id, result):
        if self.value is None:
            self.results[worker_id] = result
            return True
        else:
            if self.value == result:
                self.results[worker_id] = result
                return True

        return False

    def add_workers(self, workers: list):
        for worker in workers:
            if worker not in self.workers:
                self.workers.append(worker)

    def check_computability(self):
        if self.computable:
            return True

        for child in self.children:
            if child.value is None:
                return False

        self.computable = True

        return True

    def get_holders(self):
        if self.value is not None:
            return [worker_id for worker_id in self.results.keys() if self.results[worker_id] == self.value]

        return []

    def compute(self):
        computable = True
        for child in self.children:
            if child.value is None:
                child.compute()
                computable = False

        if computable:
            self.scheduler.schedule(self)

        return None

