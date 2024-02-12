

class Controller:
    def __init__(self, node, config: dict):
        self.node = node
        self.config = config
        self.controller = self.load_controller(config)


    def load_controller(self, config: dict):
        pass
        return 0

    def upload(self):
        pass

    def generate_token(self, resource_idn: str, non_holders: list):
        pass

    def download(self):
        pass
