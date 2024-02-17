from time import time


class Jobs:
    def __init__(self, workers: list):
        self.workers = workers
        self.tasks = {worker_id: {
            'download': {},
            'upload': {},
            'compute': {},
        } for worker_id in workers}

    def assign_jobs(self, tree_node, workers: list):
        for worker_id in workers:
            self.set_download_tasks(tree_node, worker_id)
            self.set_upload_tasks(tree_node, worker_id)
            self.set_compute_tasks(tree_node, worker_id)

    def set_download_tasks(self, tree_node, worker_id: int):
        for child in tree_node.children:
            holders = child.get_holders()
            if worker_id not in holders:
                if self.tasks[worker_id]['download'].get(child.idn) is None:
                    self.tasks[worker_id]['download'][child.idn] = {
                        'holders': holders,
                        'value': child.value,
                        'time_created': time(),
                        'time_done': None,
                    }

    def set_upload_tasks(self, tree_node, worker_id: int):
        other_workers = [w for w in tree_node.workers if w != worker_id]

        for child in tree_node.children:
            holders = child.get_holders()
            if worker_id in holders:
                non_holders_workers = [w for w in other_workers if w not in holders]
                if len(non_holders_workers) > 0:
                    if self.tasks[worker_id]['upload'].get(child.idn) is None:
                        self.tasks[worker_id]['upload'][child.idn] = {}

                    created_time = time()
                    for non_holder_worker in non_holders_workers:
                        if self.tasks[worker_id]['upload'][child.idn].get(non_holder_worker) is None:
                            self.tasks[worker_id]['upload'][child.idn][non_holder_worker] = {
                                'time_created': created_time,
                                'time_done': None,
                            }

    def set_compute_tasks(self, tree_node, worker_id: int):
        if tree_node.type == "group":
            return

        if self.tasks[worker_id]['compute'].get(tree_node.idn) is None:
            self.tasks[worker_id]['compute'][tree_node.idn] = {
                'resources': [child.idn for child in tree_node.children],
                'time_created': time(),
                'time_done': None,
            }

    def get_jobs(self, worker_id: int):
        # get jobs where time_done is None
        jobs = []
        for task_type in self.tasks[worker_id].keys():
            for task_idn, task in self.tasks[worker_id][task_type].items():
                if task_type != 'upload':
                    if task['time_done'] is None:
                        jobs.append((task_type, task_idn, task))
                else:
                    for non_holder_worker, non_holder_task in task.items():
                        if non_holder_task['time_done'] is None:
                            jobs.append((task_type, task_idn, non_holder_worker))

        return jobs

    def check_non_upload_job_validity(self, worker_id: int, task_type: str, task_idn: str):
        if self.tasks[worker_id][task_type].get(task_idn) is not None:
            if self.tasks[worker_id][task_type][task_idn]['time_done'] is not None:
                self.tasks[worker_id][task_type][task_idn]['time_done'] = time()
                return True

        return False

    def check_upload_job_validity(self, worker_id: int, task_idn: str, non_holder_worker: int):
        task_type = 'upload'

        if self.tasks[worker_id][task_type].get(task_idn) is not None:
            if self.tasks[worker_id][task_type][task_idn].get(non_holder_worker) is not None:
                if self.tasks[worker_id][task_type][task_idn][non_holder_worker]['time_done'] is not None:
                    self.tasks[worker_id][task_type][task_idn][non_holder_worker]['time_done'] = time()
                    return True

        return False

    def refresh(self):
        pass



