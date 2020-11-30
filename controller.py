

class Controller:
    
    def validate(self, request):
        if request.method == 'PUT' and request.headers.get('Content-Type') != 'application/json':
            return False   
        return True
