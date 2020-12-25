import pymongo
import redis
import logging
import logging.config

class Cache:

    def __init__(self, cache_host, cache_port):
        logging.config.fileConfig("logging.conf")
        self.logger = logging.getLogger("InstanceLogger")
        self.cache = redis.Redis(cache_host, cache_port)
    
    def exists(self, file_name):
        self.logger.debug(f'Checking presence of {file_name} in cache')
        resp = self.cache.exists(file_name)
        if not resp: self.logger.warning(f'No file named {file_name} in cache')
        return resp
        
    def get(self, file_name):
        self.logger.debug(f'Getting {file_name} from cache')
        return self.cache.get(file_name)
       
    def put(self, file_name, data):
        self.logger.debug(f'Putting file {file_name} to cache with value {data}')
        self.cache.set(file_name, data)
    
    def delete(self, file_name):
        self.logger.debug(f'Deleting file {file_name} from cache')
        self.cache.delete(file_name)

class DBase:

    def __init__(self, database_port):
        logging.config.fileConfig("logging.conf")
        self.logger = logging.getLogger("InstanceLogger")
        mongoClient = pymongo.MongoClient(host='mongo', port=database_port)
        self.dbase = mongoClient["hw9"]["files"]
        
    def get(self, file_name):
        self.logger.debug(f'Getting file {file_name} from database')
        dbase_resp = self.dbase.find_one({'key':file_name})
        if dbase_resp:
            return dbase_resp['value']
        else:
            self.logger.error(f'No file named {file_name} in database')
            return None
    
    def put(self, file_name, data):
        if self.dbase.find_one({'key': file_name}):
            self.logger.info(f'Overriding {file_name}')
            self.dbase.delete_many({'key':file_name})
        self.dbase.insert_one({'key': file_name, 'value': data})
    
    def delete(self, file_name):
        self.logger.debug(f'Deleting file {file_name} from database')
        if not self.dbase.find_one({'key': file_name}):
            self.logger.info(f'No such file {file_name} to delete in database')
        self.dbase.delete_many({'key':file_name})
