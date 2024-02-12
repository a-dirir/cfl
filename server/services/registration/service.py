
from server.services.registration.controllers.node import Node
from server.services.registration.controllers.process import Process


class Registration:
    def __init__(self):
        self.name = 'Registration'

        self.handlers = {
            'Node': Node(),
            'Process': Process()
        }

    def handle(self, payload: dict, handler: str, method: str):
        if self.handlers.get(handler) is None:
            return {'error': 'API Handler is invalid'}, 400

        try:
            handler_method = getattr(self.handlers[handler], method)
            msg, status_code = handler_method(payload)
            return msg, status_code
        except AttributeError as e:
            print(e)
            return {'error': 'API method is invalid'}, 400
        except Exception as e:
            print(e)
            return {'error': 'Some error happened, please try again'}, 400




