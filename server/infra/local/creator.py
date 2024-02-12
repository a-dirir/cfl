import json
from os import path, mkdir
import shutil

from crypto.communication_handler import CommunicationHandler
from utils.util import c2s


class LocalServerCreator:
    """Local infrastructure."""

    def __init__(self, config: dict) -> None:
        self.type = "local_creator"
        self.config = config

    def create(self) -> None:

        """Create infrastructure."""
        directory = self.config.get("directory")
        # create data directory if not exists
        if not path.exists(directory):
            mkdir(path.join(directory))
            # create api-server's crypto keys
            communicator = CommunicationHandler(0, directory, True)
            communicator.encryptor.store_keys(directory)
            communicator.signer.store_keys(directory)
            # create api-server registration
            nodes = {
                0: {
                    "pek": c2s(communicator.encryptor.get_public_key()),
                    "psk": c2s(communicator.signer.get_public_key()),
                    "info": {"name": "api-server"}
                }
            }
            # create registration.json file
            with open(path.join(directory, "nodes.json"), "w") as f:
                f.write(json.dumps(nodes))

            # create processes.json file
            processes = {}
            with open(path.join(directory, "processes.json"), "w") as f:
                f.write(json.dumps(processes))



    def destroy(self) -> None:
        """Destroy infrastructure."""
        directory = self.config.get("directory")
        # remove registration.json file if exists
        if path.exists(directory):
            shutil.rmtree(directory)

