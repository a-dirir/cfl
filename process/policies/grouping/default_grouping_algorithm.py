import pickle
from utils.util import c2s, hash_msg


class DefaultGroupingAlgorithm:
    def __init__(self, nodes: list, config: dict):
        self.nodes = nodes
        self.config = config

        self.process_id = self.config['process_id']
        self.round_num = self.config['round_num']
        self.group_size = self.config['group_size']
        self.round_randomness = self.config['round_randomness']

        self.groups = []


    def apply(self):
        # shuffle the list using hashing
        hash_of_nodes = []
        hash_mappings = {}
        for node_id in self.nodes:
            node_value = node_id + self.process_id + self.round_num * self.round_randomness
            hash_value = c2s(hash_msg(pickle.dumps(node_value)))
            hash_of_nodes.append(hash_value)
            hash_mappings[hash_value] = node_id

        hash_of_nodes.sort()

        new_nodes_list = []

        for hash_value in hash_of_nodes:
            new_nodes_list.append(hash_mappings[hash_value])

        # divide the list into groups, remianing nodes will be added to the last group
        num_groups = len(self.nodes) // self.group_size
        remaining_nodes = len(self.nodes) % self.group_size

        for i in range(num_groups):
            self.groups.append(new_nodes_list[i * self.group_size: (i + 1) * self.group_size])

        if remaining_nodes > 0:
            for i in range(remaining_nodes):
                self.groups[i].append(new_nodes_list[-remaining_nodes + i])

        return self.groups

