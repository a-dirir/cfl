from client.node import Node

n = Node(node_id=1, root_dir="D:\\CFL")
print(n.working_dir)

# n.registration.create_process(config={'name': 'test', 'args': ['arg1', 'arg2']})
n.registration.participate(0,
                           {"storage":{"type":"local",
                                       "endpoint":f"http://localhost:{5000+n.node_id}"}})
print(n.registration.get_processes())