from process.process import Process


class SingleGroupRunner:
    def __init__(self):
        self.config = self.create_config()
        self.nodes_inputs = self.create_nodes_inputs()
        self.process = Process(self.nodes_inputs, self.config)
        self.run()

    @staticmethod
    def create_config():
        config = {
            'num_blocks': 2,
            'num_workers': 2,
            'num_judges': 1,
            'process_id': 1,
            'round_num': 1,
            'group_size': 4,
            'round_randomness': 0,
        }
        return config

    def create_nodes_inputs(self):
        nodes_inputs = {}
        for node_id in range(1, 5):
            nodes_inputs[node_id] = {}
            for block_num in range(1, self.config['num_blocks'] + 1):
                nodes_inputs[node_id][block_num] = {}
                for complement_idn in range(1, 3):
                    nodes_inputs[node_id][block_num][complement_idn] = f"{node_id*3 + block_num*5 + complement_idn*7}"

        return nodes_inputs

    def run(self):
        self.process.add_results({})
        worker_results = self.complete_work()

        self.process.add_results(worker_results)
        worker_results = self.complete_work()

        self.process.add_results(worker_results)
        worker_results = self.complete_work()

        self.process.add_results(worker_results)
        worker_results = self.complete_work()

        # self.process.print_tree()



    def complete_work(self):
        self.process.scheduler.compute()
        results = {i: {} for i in range(1, 5)}
        for worker_id in range(1, 5):
            worker_jobs = self.process.get_jobs(worker_id)
            print('Job => ', worker_id, worker_jobs)
            for job in worker_jobs:
                job_type = job[0]
                if job_type == 'download':
                    pass
                elif job_type == 'upload':
                    pass
                elif job_type == 'compute':
                    results[worker_id][job[1]] = "1"


        return results


sgr = SingleGroupRunner()
