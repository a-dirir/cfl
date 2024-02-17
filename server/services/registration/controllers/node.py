

class Node:
    def __init__(self):
        pass

    def createNode(self, payload: dict):
        data = payload['data']
        db = payload['db']

        nodes = db.get('nodes')
        node_id = len(nodes)

        db.create('nodes', {
            'node_id': node_id,
            'pek': data['pek'],
            'psk': data['psk'],
            'info': data['info']
        })

        return {"node_id": node_id}, 200

    def getNode(self, payload: dict):
        data = payload['data']
        db = payload['db']

        node = db.get('nodes', data['node_id'])
        print(44,node)
        if node is None:
            return {'error': 'Node not found'}, 400

        return node, 200

    def getNodes(self, payload: dict):
        db = payload['db']

        nodes = db.get('nodes')
        return nodes, 200

    def updateNode(self, payload: dict):
        data = payload['data']
        db = payload['db']

        node_data = db.get('nodes', data['node_id'])
        node_data['info'] = data['info']

        updated = db.set('nodes', data['node_id'], node_data)

        if not updated:
            return {'error': 'Failed to update Node'}, 400


        return {}, 200

    def deleteNode(self, payload: dict):
        data = payload['data']
        db = payload['db']

        deleted = db.delete('nodes', data['node_id'])

        if not deleted:
            return {'error': 'Failed to delete Node'}, 400
        
        return {}, 200





