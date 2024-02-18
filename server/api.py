from flask import Flask, request, jsonify
from flask_cors import CORS

from crypto.communication_handler import CommunicationHandler
from server.router import Router
from utils.util import c2b, c2s


class Server:
    def __init__(self, communicator: CommunicationHandler, db):
        self.nodes = {}
        self.communicator = communicator
        self.db = db

        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.router = Router()
        self.routes()
        self.app.run(host="0.0.0.0", port=8080)

    def load_node(self, node_id):
        node = self.db.get("nodes", node_id)
        if node is None:
            return False

        self.nodes[node_id] = node

        return True

    def routes(self):
        @self.app.route('/info', methods=['GET'])
        def index():
            # return public key of the server
            msg = {
                "pek": c2s(self.communicator.encryptor.get_public_key()),
                "psk": c2s(self.communicator.signer.get_public_key())
            }

            return jsonify(msg=msg, status_code=200)

        @self.app.route('/', methods=['POST'])
        def app():
            # load json data from request
            request_msg: dict = request.get_json()

            # check if signature key belongs to node_id
            node_id = request_msg.get('node_id')
            signature_key = request_msg.get('sk')
            encryption_key = request_msg.get('ek')

            if node_id is None or signature_key is None:
                return jsonify(msg='Request is missing node_id or signature key', status_code=401)

            if node_id > 0:
                # check if node_id is registered
                if node_id not in self.nodes:
                    loaded = self.load_node(node_id)
                    if not loaded:
                        return jsonify(msg='Node is not registered', status_code=401)

                # check if signature key belongs to node_id
                if signature_key != self.nodes[node_id]['psk']:
                    return jsonify(msg='Signature key does not belong to node_id', status_code=401)

            # check if the request is authenticated
            msg = self.communicator.ingress(request_msg)

            if msg is None:
                return jsonify(msg='Authentication failed', status_code=401)

            payload = {'msg': msg, 'db': self.db, 'data': msg['data'],
                       'node_id': node_id, 'signature_key': signature_key}

            # route the request to the appropriate service, controller and method
            msg, status_code = self.router.route(payload)

            # encrypt the response
            msg = self.communicator.outgress(msg, c2b(encryption_key))

            # return a flask response object to the client
            if status_code == 200:
                return jsonify(msg=msg, status_code=status_code)
            else:
                return jsonify(msg=msg, status_code=status_code)
