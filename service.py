import repository

class Service:
    
    def __init__(self):
        self.repo = repository.Repository()
    
    def get(self, file_name):
        if self.repo.exists_in_cache(file_name):
            return self.repo.get_from_cache(file_name)
        else:
            return self.repo.get_from_dbase(file_name)
    
    def put(self, file_name, data, dest = 'dbase'):
        if dest == 'cache':
            self.repo.put_to_cache(file_name, data)
        elif dest == 'dbase':
            self.repo.put_to_dbase(file_name, data)
    
    def delete(self, file_name):
    	self.repo.delete(file_name)
