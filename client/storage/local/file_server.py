import pickle
from flask import send_file, request, Flask, make_response
from os import path

from client.node import Node


class FileServer:
    def __init__(self, node: Node, storage_dir: str, port: int = -1,
                 host: str = "0.0.0.0", file_extension: str = "txt"):
        self.node = node
        self.storage_dir = storage_dir
        self.node_id = node.node_id
        self.file_extension = file_extension

        self.app = Flask(__name__)
        self.routes()

        if port == -1:
            port = 5000 + self.node_id

        self.app.run(port=port, host=host)

    def verify_token(self, token: dict, requester_id: int):
        access = token['access']
        signature = token['signature']

        if requester_id != access['requester_id']:
            return False

        signature_valid = self.node.communicator.signer.verify_other_signatures(
            signature,
            pickle.dumps(access),
            self.node.communicator.signer.get_public_key()
        )

        return signature_valid

    def routes(self):
        @self.app.route('/', methods=["POST"])
        def get():
            request_msg = request.get_json()
            requester_id = request_msg['node_id']

            try:
                msg = self.node.communicator.ingress(request_msg)

                if msg is None:
                    return make_response({"Error": "Authentication Fails"}, 401)

                if not self.verify_token(msg['token'], requester_id):
                    return make_response({"Error": "Token is not valid"}, 401)

                resource_idn = msg['token']['access']['resource_idn']

                filename = f"R_{resource_idn}.{self.file_extension}"

                response = make_response(send_file(path.join(self.storage_dir, filename)))

                # comment these 3 lines if you don't want to send info
                self.node.file_handler.load_files_info(self.storage_dir)
                meta_data = self.node.file_handler.files[filename]
                response.headers['info'] = self.node.communicator.outgress(meta_data, request_msg['ek'])

                return response
            except Exception as e:
                print(f"Error: {e}")
                return make_response(f"Error: {e}", 401)


