from utils import Request, Responce

class Service:
    
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database

    def get(self, request):
        resp = Responce(request)
        if self.cache.exists(request.key):
            resp.data = self.cache.get(request.key)
            resp.is_successful = True
        else:
            data = self.database.get(request.key)
            if data != None:
                self.cache.put(request.key, data)
                resp.data = data
                resp.is_successful = True
        return resp

    def put(self, request):
        if self.cache.exists:
            self.cache.delete(request.key)
        self.database.put(request.key, request.data)
        return Responce(request, is_successful = True)  

    def delete(self, request):
        if self.cache.exists:
            self.cache.delete(request.key)
        self.database.delete(request.key)
        return Responce(request, is_successful = True)  
