from process.state.computation import Computation
from process.state.group import Group
from process.state.root import Root


class State:
    def __init__(self, scheduler, groups: list, config: dict):
        self.scheduler = scheduler
        self.groups = groups
        self.num_blocks = config['num_blocks']
        self.num_complements = config['num_complements']
        self.root = None

        self.tree_lookup = {}

        self.create_tree()

    def create_tree(self):
        groups = []
        for group_index, group in enumerate(self.groups):
            blocks = self.create_blocks_nodes(group, group_index)

            group_computation = Group(num_blocks=self.num_blocks, workers=list(group.keys()),
                                      children=blocks, scheduler=self.scheduler)

            self.tree_lookup[group_computation.idn] = [group_index]

            groups.append(group_computation)

        self.root = Root(children=groups, scheduler=self.scheduler)

    def create_leaf_nodes(self, group_workers: list, group_index: int):
        leaf_nodes = {block_num: {} for block_num in range(1, self.num_blocks + 1)}

        for block_num in range(1, self.num_blocks + 1):
            for complement_num in range(1, self.num_complements + 1):
                for worker_index, worker_id, in enumerate(group_workers):
                    if leaf_nodes[block_num].get(complement_num) is None:
                        leaf_nodes[block_num][complement_num] = []

                    leaf_node_idn = f"D_{worker_id}-{block_num}-{complement_num}"

                    leaf_computation = Computation(block_num=block_num, group_index=group_index, children=[],
                                                   scheduler=self.scheduler, idn=leaf_node_idn)
                    leaf_computation.workers = [worker_id]

                    leaf_nodes[block_num][complement_num].append(leaf_computation)

                    self.tree_lookup[leaf_computation.idn] = [group_index, block_num-1, complement_num-1, worker_index]

        return leaf_nodes

    def create_blocks_nodes(self, group_workers: list, group_index: int = None):
        blocks = []
        leaf_nodes = self.create_leaf_nodes(group_workers, group_index)

        for block_num in range(1, self.num_blocks + 1):
            complements = []
            for complement in leaf_nodes[block_num].values():
                complements.append(Computation(block_num=block_num, group_index=group_index,
                                               children=complement, scheduler=self.scheduler))

                self.tree_lookup[complements[-1].idn] = [group_index, block_num-1, len(complements)-1]

            if len(complements) > 1:
                block_computation = Computation(block_num=block_num, group_index=group_index,
                                                children=complements, scheduler=self.scheduler)
            elif len(complements) == 1:
                block_computation = complements[0]
            else:
                block_computation = None

            self.tree_lookup[block_computation.idn] = [group_index, block_num-1]

            blocks.append(block_computation)

        return blocks

    def add_results(self, worker_id: int, idn: str, value: str):
        tree_node = self.root
        for path in self.tree_lookup[idn]:
            tree_node = tree_node.children[path]
        tree_node.add_result(worker_id, value)

    def print_tree(self):
        self.root.print_tree()





