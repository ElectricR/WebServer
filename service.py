from utils import Request, Responce

class Service:
    
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database

    def get(self, request):
        resp = Responce(request)
        if self.cache.exists(file_name):
            resp.data = self.cache.get(file_name)
            resp.is_successful = True
        else:
            data = self.database.get(file_name)
            if data != None:
                self.cache.put(file_name, data)
                resp.data = data
                resp.is_successful = True
        return resp

    def put(self, request):
        self.database.put(file_name, data)
        return Responce(request, is_successful = True)  

    def delete(self, request):
        if self.cache.exists:
            self.cache.delete(file_name)
        self.database.delete(file_name)
        return Responce(request, is_successful = True)  
