


class DefaultConsensusAlgorithm:
    def __init__(self, config: dict = None):
        self.config = config

    def apply(self, tree_node):
        if tree_node.type == 'computation':
            return self.handle_computation(tree_node)
        else:
            return None, 0

    def handle_computation(self, computation):
        workers = computation.workers
        results = computation.results

        if len(workers) == 0:
            return None, self.config['num_workers']

        if len(results) < len(workers):
            return None, 0
        else:
            return self.get_majority_results(results)

    def get_majority_results(self, results: dict):
        # find how many times each result appears
        result_counts = {}
        maximum_count = 0
        for result in results.values():
            if result not in result_counts:
                result_counts[result] = 1
            else:
                result_counts[result] += 1

            if result_counts[result] >= maximum_count:
                maximum_count = result_counts[result]

        # find the results that appear the most
        majority_results = []
        for result, count in result_counts.items():
            if count == maximum_count:
                majority_results.append(result)

        # if there is only one result that appears the most, return it
        if len(majority_results) == 1:
            return majority_results[0], 0
        else:
            return None, self.config['num_judges']



