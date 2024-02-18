from infra.server.local.loader import LocalServerLoader
from server.database.local_db import LocalDB
from server.api import Server


if __name__ == '__main__':
    root_dir = "D:\\CFL"
    server_loader = LocalServerLoader({'root_dir': root_dir})
    communication_handler = server_loader.load()
    db = LocalDB(server_loader.directory)
    server = Server(communication_handler, db)

