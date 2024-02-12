from os import path, getenv, mkdir, getcwd, pardir
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from crypto.communication_handler import CommunicationHandler
from server.router import Router
from server.infra.local.loader import LocalServerLoader
from server.database.local_db import LocalDB
from utils.util import c2b


class Server:
    def __init__(self, communicator: CommunicationHandler, db):
        self.nodes = {}
        self.communicator = communicator

        self.db = db

        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.router = Router()
        self.routes()
        self.app.run(host="0.0.0.0", port=getenv("CFL_API_Server_Port"))

    def load_node(self, node_id):
        node = self.db.get("nodes", f"{node_id}")
        if node is None:
            return False

        self.nodes[node_id] = node

        return True

    def routes(self):
        @self.app.route('/', methods=['POST'])
        def app():
            # load json data from request
            request_msg: dict = request.get_json()

            # check if signature key belongs to node_id
            node_id = request_msg.get('node_id')
            signature_key = request_msg.get('sk')
            encrption_key = request_msg.get('ek')

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
            msg = self.communicator.outgress(msg, c2b(encrption_key))

            # return a flask response object to the client
            if status_code == 200:
                return jsonify(msg=msg, status_code=status_code)
            else:
                return jsonify(msg, status_code=status_code)



if __name__ == '__main__':
    dir_path = path.dirname(path.realpath(__file__))
    parent_path = path.abspath(path.join(dir_path, pardir))
    load_dotenv(path.join(parent_path, 'config.env'))

    deployment_type = getenv("Deployment_Environment")

    if deployment_type == "local":
        print("Local deployment")
        directory = path.join(getenv("Work_Directory"), 'server')
        deployment = LocalServerLoader({'directory': directory})
        communication_handler = deployment.load()
        db = LocalDB(directory)
        server = Server(communication_handler, db)


