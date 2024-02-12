from process.process import Process


class Manager:
    def __init__(self):
        self.processes = {}

    def AddResources(self, payload: dict):
        data = payload['data']
        db = payload['db']

        process_id = data['process_id']
        node_id = data['node_id']
        resources = data['resources']

        if process_id not in self.processes:
            # Get config from db
            process_data = db.get('process', data['process_id'])
            self.processes[process_id] = Process(process_data['config'], process_data['participants'])

        self.processes[process_id].add_resources(node_id, resources)

        return {}, 200

    def GetJobs(self, payload: dict):
        data = payload['data']

        process_id = data['process_id']
        node_id = data['node_id']

        if process_id not in self.processes:
            return {'error': 'Process not found or not started'}, 400

        jobs = self.processes[process_id].get_jobs(node_id)

        return jobs, 200

    def AddTokens(self, payload: dict):
        data = payload['data']

        process_id = data['process_id']
        node_id = data['node_id']
        tokens = data['tokens']

        if process_id not in self.processes:
            return {'error': 'Process not found or not started'}, 400

        self.processes[process_id].add_tokens(node_id, tokens)

        return {}, 200

    def GetTokens(self, payload: dict):
        data = payload['data']

        process_id = data['process_id']
        node_id = data['node_id']

        if process_id not in self.processes:
            return {'error': 'Process not found or not started'}, 400

        tokens = self.processes[process_id].get_tokens(node_id)

        return tokens, 200

    def SubmitJobs(self, payload: dict):
        data = payload['data']

        process_id = data['process_id']
        node_id = data['node_id']
        results = data['results']

        if process_id not in self.processes:
            return {'error': 'Process not found or not started'}, 400

        self.processes[process_id].submit_jobs(node_id, results)

        return {}, 200

