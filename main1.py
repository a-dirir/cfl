from os import path, pardir

from dotenv import load_dotenv

from client.node import Node

dir_path = path.dirname(path.realpath(__file__))
load_dotenv(path.join(dir_path, 'config.env'))
n = Node(1)
# n.registration.delete_node()
# print(n.registration.get_node(1))

# n.registration.create_process({"dd": "dd"})
# n.registration.participate(0)
# print(n.registration.get_process(0))

# n.file_handler.set_directory(path.join(n.working_dir, "Processes"))
#
#
# # data = b"Hello World11"
# # n.file_handler.save_file(data, "test11.txt")
#
# print(n.file_handler.files)
#
# print(n.file_handler.read_file("test11.txt")[0])

# print(n.registration.get_nodes())

# from client.storage.local.server import Server
#
# s = Server(n, path.join(n.working_dir, "Processes"))

import requests

from utils.util import c2s
import pickle

# access = {
#         'requester_id': 2,
#         'resource_idn': 'test',
#     }
# signature = c2s(n.communicator.signer.sign_message(pickle.dumps(access)))
# msg = {
#     "token": {
#         'access': access,
#         'signature': signature
#     }
# }


nn = Node(2)
# con = nn.download_file(msg, n.communicator.encryptor.get_public_key(), n.communicator.signer.get_public_key(), "test",
#                        "D:\CFL\client\\Node_2\Processes", "http://172.17.1.16:5001")
#
# print(con)

from client.storage.local.local_client import LocalClient

c = LocalClient(n)

token = c.generate_token("test8788", [2])[2]
# print(token)



# c.upload({"test8788": pickle.dumps({"s": "ss"})}, {"storage_dir": path.join(n.working_dir, "Processes")})

cc = LocalClient(nn)

con = cc.download("test8788", {1:token}, {"participants": {1: {"pek": n.communicator.encryptor.get_public_key(),
                                                            "psk": n.communicator.signer.get_public_key(),
                                                            "storage": {"end_point": "http://192.168.0.160:5001"}}},
                                                            "storage_dir": path.join(nn.working_dir, "Processes")})

print(con)

