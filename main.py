from os import path, pardir

from dotenv import load_dotenv

from client.node import Node
#
# dir_path = path.dirname(path.realpath(__file__))
# load_dotenv(path.join(dir_path, 'config.env'))
# n = Node(1)
# n.file_handler.load_files_info(path.join(n.working_dir, "Processes"))
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

# from client.storage.local.local_server import LocalServer
#
# s = LocalServer(n, path.join(n.working_dir, "Processes"))



# if __name__ == '__main__':
#     dir_path = path.dirname(path.realpath(__file__))
#     parent_path = path.abspath(path.join(dir_path, pardir))
#     load_dotenv(path.join(parent_path, 'config.env'))
#
#     deployment_type = getenv("Deployment_Environment")
#
#     if deployment_type == "local":
#         print("Local deployment")
#         directory = path.join(getenv("Work_Directory"), 'server')
#         deployment = LocalServerLoader({'directory': directory})
#         communication_handler = deployment.load()
#         db = LocalDB(directory)
#         server = Server(communication_handler, db)
