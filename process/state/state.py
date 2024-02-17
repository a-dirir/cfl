from process.state.resource import Resource
from process.state.computation import Computation
from process.state.group import Group
from process.state.root import Root


class State:
    def __init__(self, scheduler, initial_groups: list, config: dict):
        self.scheduler = scheduler
        self.groups = initial_groups
        self.num_blocks = config['num_blocks']
        self.root = None

        self.tree_lookup = {}

        self.build_tree()

    def build_tree(self):
        groups = []
        for group_index, group in enumerate(self.groups):
            blocks = self.build_blocks_nodes(group, group_index)

            group_computation = Group(num_blocks=self.num_blocks, nodes=list(group.keys()),
                                      children=blocks, scheduler=self.scheduler)

            self.tree_lookup[group_computation.idn] = [group_index]

            groups.append(group_computation)

        self.root = Root(children=groups, scheduler=self.scheduler)

    def create_resources(self, nodes_inputs: dict):
        resources = {block_num: {} for block_num in range(1, self.num_blocks + 1)}

        for node_id, node_input in nodes_inputs.items():
            for block_num in range(1, self.num_blocks + 1):
                for complement_idn, complement_value in nodes_inputs[node_id][block_num].items():
                    if resources[block_num].get(complement_idn) is None:
                        resources[block_num][complement_idn] = []

                    resources[block_num][complement_idn].append(
                        Resource(value=complement_value, holders=[node_id])
                    )

        return resources

    def build_blocks_nodes(self, group: dict, group_index: int = None):
        blocks = []
        resources = self.create_resources(group)

        for block_num in range(1, self.num_blocks + 1):
            complement_computations = []
            for complement_resources in resources[block_num].values():
                complement_computations.append(Computation(block_num=block_num, group_index=group_index,
                                                           children=complement_resources, scheduler=self.scheduler))
                self.tree_lookup[complement_computations[-1].idn] = [group_index, block_num-1,
                                                                     len(complement_computations)-1]

            if len(complement_computations) > 1:
                block_computation = Computation(block_num=block_num, group_index=group_index,
                                                children=complement_computations, scheduler=self.scheduler)
            elif len(complement_computations) == 1:
                block_computation = complement_computations[0]
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





