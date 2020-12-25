class Request:

    def __init__(self, request_type, key = '', data = ''):
        self.request_type = request_type
        self.data = data
        self.key = key

class Responce:

    def __init__(self, request, data = None, is_successful = False):
        self.request = request
        self.data = data
        self.is_successful = is_successful 
