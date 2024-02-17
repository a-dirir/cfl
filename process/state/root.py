import pickle
from hashlib import sha256


class Root:
    def __init__(self, children: list, scheduler):
        self.children = children
        self.scheduler = scheduler

        self.idn = None
        self.value = None

        self.type = "root"

        self.set_identifier()

    def set_identifier(self):
        # get idns of children, sort them, convert to binary using pickle, hash the sorted list
        idns = [child.idn for child in self.children]
        idns.sort()
        idns = pickle.dumps(idns)
        self.idn = sha256(idns).hexdigest()

    def compute(self):
        computable = True
        for child in self.children:
            if child.value is None:
                child.compute()
                computable = False

        if computable:
            self.scheduler.schedule(self)

        return None

    def check_commit(self):
        for child in self.children:
            if not child.check_commit():
                return False

        if len(self.children) > 1:
            return False

        return True

    def print_tree(self):
        queue = [self]
        while queue:
            node = queue.pop(0)
            print(f"{node.idn} {node.value} {node.type}")
            for child in node.children:
                queue.append(child)





