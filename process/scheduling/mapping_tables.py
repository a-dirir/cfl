from utils.util import create_mapping_table


class MappingTables:
    def __init__(self, groups: list, config: dict):
        self.groups = groups
        self.config = config

        self.num_blocks = config['num_blocks']

        self.mapping_tables = []
        self.cursor = {}

        self.build_mapping_tables()

    def build_mapping_tables(self):
        for index, group in enumerate(self.groups):
            mapping_table = create_mapping_table(self.num_blocks, len(group), group)
            self.mapping_tables.append(mapping_table)

            self.cursor[index] = []
            for block_num in range(1, self.num_blocks+1):
                self.cursor[index].append({
                    'initial_group': index,
                    'initial_position': 0,
                    'current_group': index,
                    'current_position': 0,
                })

    def get_next_workers(self, tree_node, num_new_workers: int):
        workers = []

        # if the tree_node has computation child, then just return the workers of all computation children
        if tree_node.children[0].type == 'computation':
            for child in tree_node.children:
                for child_worker in child.workers:
                    if child_worker not in workers:
                        workers.append(child_worker)
            return workers

        # if the tree_node has resource child, then use mapping table to get the next workers
        elif tree_node.children[0].type == 'resource':
            return self.get_next_worker_from_mapping_table(tree_node, num_new_workers)

    def get_next_worker_from_mapping_table(self, tree_node, num_new_workers: int):
        workers = []

        group_index = tree_node.group_index
        block_num = tree_node.block_num
        current_position = self.cursor[group_index][block_num - 1]['current_position']
        current_group = self.cursor[group_index][block_num - 1]['current_group']

        for i in range(num_new_workers):
            if current_position >= len(self.mapping_tables[current_group][block_num - 1]):
                current_position = 0
                current_group = (current_group + 1) % len(self.groups)

                if current_group == self.cursor[group_index][block_num - 1]['initial_group']:
                    return []

            workers.append(self.mapping_tables[current_group][block_num - 1][current_position])
            current_position += 1

        return workers
