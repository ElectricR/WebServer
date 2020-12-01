import pymongo
import redis
import os

class Repository:

    def __init__(self):
        self.cache = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
        self.mongoClient = pymongo.MongoClient(host='mongo', port=27017)
        self.dbase = self.mongoClient["hw9"]["files"]
        
    def exists_in_cache(self, file_name):
        return self.cache.exists(file_name)
        
    def get_from_cache(self, file_name):
        return self.cache.get(file_name)
       
    def get_from_dbase(self, file_name):
        dbase_resp = self.dbase.find_one({'key':file_name})
        if dbase_resp:
            return dbase_resp['value']
            self.put_to_cache(file_name, dbase_resp['value'])
        else:
            return None
    
    def put_to_cache(self, file_name, data):
        self.cache.set(file_name, data)
        self.dbase.delete_many({'key':file_name})
        self.dbase.insert_one({'key': file_name, 'value': data})
    
    def put_to_dbase(self, file_name, data):
        self.dbase.delete_many({'key':file_name})
        self.dbase.insert_one({'key': file_name, 'value': data})
    
    def delete(self, file_name):
        self.cache.delete(file_name)
        self.dbase.delete_many({'key':file_name})
