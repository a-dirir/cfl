import json
from os import path


class LocalDB:
    def __init__(self, directory):
        self.directory = directory
        self.nodes = {}
        self.processes = {}
        self.load()

    def load(self):
        with open(path.join(self.directory, "nodes.json"), "r") as f:
            self.nodes = json.load(f)

        with open(path.join(self.directory, "processes.json"), "r") as f:
            self.processes = json.load(f)

        return None

    def set(self, table_name, row_id, data):
        if table_name == "nodes":
            self.nodes[row_id] = data
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.nodes))
            return True

        if table_name == "processes":
            self.processes[row_id] = data
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.processes))
            return True

        return False

    def get(self, table_name, row_id=-1):
        if table_name == "nodes":
            if row_id == -1:
                return self.nodes
            if row_id not in self.nodes:
                return None
            return self.nodes[row_id]

        if table_name == "processes":
            if row_id == -1:
                return self.processes

            if row_id not in self.processes:
                return None
            return self.processes[row_id]

        return None

    def create(self, table_name, data):
        if table_name == "nodes":
            row_id = len(self.nodes)
            self.nodes[row_id] = data
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.nodes))
            return True

        if table_name == "processes":
            row_id = len(self.processes)
            self.processes[row_id] = data
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.processes))
            return True

        return False

    def delete(self, table_name, row_id):
        if table_name == "nodes":
            if row_id not in self.nodes:
                return False
            del self.nodes[row_id]
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.nodes))
            return True

        if table_name == "processes":
            if row_id not in self.processes:
                return False
            del self.processes[row_id]
            with open(path.join(self.directory, table_name + ".json"), "w") as f:
                f.write(json.dumps(self.processes))
            return True

        return False