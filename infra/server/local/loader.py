from os import path
from crypto.communication_handler import CommunicationHandler
from infra.server.local.creator import LocalServerCreator


class LocalServerLoader:
    """Local infrastructure."""

    def __init__(self, config: dict) -> None:
        self.type = "local_loader"
        self.config = config
        self.directory = None

    def load(self):
        """Load infrastructure."""
        root_dir = self.config.get("root_dir")
        self.directory = path.join(root_dir, "server")

        # create data directory if not exists
        if not path.exists(self.directory):
            creator = LocalServerCreator({'directory': self.directory})
            creator.create()

        # load api-server's crypto keys
        communicator = CommunicationHandler(0, self.directory, False)

        return communicator
