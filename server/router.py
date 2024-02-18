from server.services.registration.service import Registration
from server.services.process.service import Process



class Router:
    def __init__(self):
        self.services = {
            'Registration': Registration(),
            'Process': Process()
        }


    def route(self, payload: dict):
        access = payload['msg']['access']

        action = access.split(':')
        # extract service, controller and method from request action
        service = str(action[0]); handler = str(action[1]); method = str(action[2])

        if self.services.get(service) is None:
            return {'error': 'API Service is invalid'}, 400

        msg, status_code = self.services[service].handle(payload, handler, method)

        return msg, status_code
