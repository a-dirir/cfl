import json
from os import path, mkdir
import shutil

from crypto.communication_handler import CommunicationHandler
from server.infra.local.creator import LocalServerCreator


class LocalServerLoader:
    """Local infrastructure."""

    def __init__(self, config: dict) -> None:
        self.type = "local_loader"
        self.config = config

    def load(self) -> CommunicationHandler:

        """Load infrastructure."""
        directory = self.config.get("directory")
        # create data directory if not exists
        if not path.exists(directory):
            creator = LocalServerCreator({'directory': directory})
            creator.create()

        # load api-server's crypto keys
        communicator = CommunicationHandler(0, directory, False)

        return communicator
