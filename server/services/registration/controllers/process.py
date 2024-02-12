

class Process:
    def __init__(self):
        pass

    def createProcess(self, payload: dict):
        data = payload['data']
        db = payload['db']

        processes = db.get('processes')

        process_id = len(processes)

        db.create('processes', {
            'process_id': process_id,
            'config': data['config'],
            'participants': [],
        })


        return {'process_id': process_id}, 200

    def getProcess(self, payload: dict):
        data = payload['data']
        db = payload['db']

        process = db.get('processes', data['process_id'])

        if process is None:
            return {'error': 'Process not found'}, 400

        return process, 200

    def getProcesses(self, payload: dict):
        db = payload['db']

        process = db.get('processes')

        return process, 200

    def updateProcess(self, payload: dict):
        data = payload['data']
        db = payload['db']

        process_data = db.get('processes', data['process_id'])
        process_data['config'] = data['config']

        updated = db.set('processes', data['process_id'], process_data)

        if not updated:
            return {'error': 'Failed to update Process'}, 400


        return {}, 200

    def deleteProcess(self, payload: dict):
        data = payload['data']
        db = payload['db']

        deleted = db.delete('processes', data['process_id'])

        if not deleted:
            return {'error': 'Failed to delete Process'}, 400
        
        return {}, 200

    def Participate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        process_data = db.get('processes', data['process_id'])

        if data['node_id'] in process_data['participants']:
            return {'error': 'Participant already in Process'}, 400

        process_data['participants'].append(data['node_id'])

        updated = db.set('processes', data['process_id'], process_data)

        if not updated:
            return {'error': 'Failed to add Participant'}, 400

        return {}, 200



