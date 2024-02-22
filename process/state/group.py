import pickle
from hashlib import sha256


class Group:
    def __init__(self, num_blocks: int, workers: list, children: list, scheduler):
        self.type = "group"
        self.idn = None
        self.value = None

        self.num_blocks = num_blocks
        self.workers = workers
        self.children = children
        self.scheduler = scheduler

        self.set_identifier()

    def set_identifier(self):
        # get idns of children, sort them, convert to binary using pickle, hash the sorted list
        idns = [child.idn for child in self.children]
        idns.sort()
        idns = pickle.dumps(idns)
        self.idn = sha256(idns).hexdigest()

    def check_computability(self):
        for child in self.children:
            if child.value is None:
                return False

        return True

    def compute(self):
        computable = True
        for child in self.children:
            if child.value is None:
                child.compute()
                computable = False

        if computable:
            self.scheduler.schedule(self)

        return None

    def get_holders(self):
        blocks = {}
        for child in self.children:
            blocks[child.block_num] = {
                "idn": child.idn,
                "holders": child.get_holders(),
                "value": child.value
            }

        return blocks

    def check_commit(self):
        if self.value is not None:
            return True

        # every registration in the group must have all blocks
        for child in self.children:
            if child.value is None:
                return False

            holders = child.get_holders()
            for worker in self.workers:
                if worker not in holders:
                    return False

        self.value = 'Committed'

        return True





