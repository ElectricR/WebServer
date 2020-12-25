from time import sleep
from utils import Request


class Controller:

    def __init__(self, service):
        self.service = service

    def handle_wait(self):
        sleep(20)
        return 'Hello there', 200

    def handle_get(self, file_name):
        service_responce = self.service.get(Request('GET', key=file_name))
        if service_responce.is_successful:
            return service_responce.data, 200
        else:
            return '', 404

    def handle_put(self, flask_request, file_name, data):
        if not self.validate(flask_request):
            return '', 400
        service_responce = self.service.put(
            Request('PUT', key=file_name, data=data))
        if service_responce.is_successful:
            return '', 201

    def handle_delete(self, file_name):
        service_responce = self.service.delete(
            Request('DELETE', key=file_name))
        if service_responce.is_successful:
            return '', 204

    def validate(self, request):
        if request.method == 'PUT' and \
                request.headers.get('Content-Type') != 'application/json':
            return False
        return True
