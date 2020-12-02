import pymongo
import redis
import os
import logging
import logging.config

class Repository:

    def __init__(self):
        logging.config.fileConfig("logging.conf")
        self.logger = logging.getLogger("InstanceLogger")
        self.cache = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
        self.mongoClient = pymongo.MongoClient(host='mongo', port=27017)
        self.dbase = self.mongoClient["hw9"]["files"]
        
    def exists_in_cache(self, file_name):
        self.logger.debug(f'Checking presence of {file_name} in cache')
        resp = self.cache.exists(file_name)
        if not resp: self.logger.warning(f'No file named {file_name} in cache')
        return resp
        
    def get_from_cache(self, file_name):
        self.logger.debug(f'Getting {file_name} from cache')
        return self.cache.get(file_name)
       
    def get_from_dbase(self, file_name):
        self.logger.debug(f'Getting file {file_name} from database')
        dbase_resp = self.dbase.find_one({'key':file_name})
        if dbase_resp:
            return dbase_resp['value']
            self.put_to_cache(file_name, dbase_resp['value'])
        else:
            self.logger.error(f'No file named {file_name} in database')
            return None
    
    def put_to_cache(self, file_name, data):
        self.logger.debug(f'Putting file {file_name} to cache with value {data}')
        self.cache.set(file_name, data)
        self.put_to_dbase(file_name, data)
    
    def put_to_dbase(self, file_name, data):
        if self.dbase.find_one({'key': file_name}):
            self.logger.info(f'Overriding {file_name}')
            self.dbase.delete_many({'key':file_name})
        self.dbase.insert_one({'key': file_name, 'value': data})
    
    def delete(self, file_name):
        self.logger.debug(f'Deleting file {file_name}')
        if not self.dbase.find_one({'key': file_name}):
            self.logger.info(f'No such file {file_name} to delete')
        self.cache.delete(file_name)
        self.dbase.delete_many({'key':file_name})
