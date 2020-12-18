#!/usr/bin/env python3
from flask import Flask, request
import requests as req
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import base64
import json
import jwt
import os

app = Flask(__name__)

INSTANCE_COUNT = int(os.environ["INSTANCE_COUNT"])

def get_url(file_name):
    instance = hash(file_name) % INSTANCE_COUNT + 1
    return 'http://{0}:{1}/storage/{2}'.format(f'pm-default-server-container-{str(instance)}', f'{int(os.environ["PORT"]) + instance}', file_name)

def get_wait_url():
    return 'http://{0}:{1}/wait'.format(f'pm-default-server-container-1', f'{int(os.environ["PORT"]) + 1}')

class Balancer:
    
    def __init__(self):
        self.users = {'killer':'qwerty123', 'vasya':'123'}
        self.usr_tokens = {}
        
        retry_strategy = Retry(total=4, backoff_factor=2)
        adapter= HTTPAdapter(max_retries=retry_strategy)
        self.http = req.Session()
        self.http.mount("http://", adapter)
    
    def authorize(self, request):
        value = request.headers.get('Authorization')
        if value == None: return '', 401
        
        value = value.split()
        if len(value) != 2 and value[0] != 'Basic': return '', 401
        
        u,p = base64.standard_b64decode(value[1]).decode().split(':')
        if u in self.users and self.users[u] == p:
            j = jwt.encode({'name':u, 'role':'write'}, 'supersecret', algorithm='HS256')
            self.usr_tokens[u] = j
            return j, 200
        else:
            return '', 401
            
    def check_JWT_auth(self, auth):
        j = jwt.decode(auth, 'supersecret', algorithms=['HS256'])
        if self.usr_tokens[j['name']] == auth.encode() and j['role'] == 'write':
            return True
        else:
            return False
    
    def wait_req(self):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
            
        try:
            resp = self.http.get(get_wait_url(), timeout=1)
        except req.exceptions.ConnectionError:
            return '', 408
            
        return resp.text, resp.status_code
            
    def get(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
        try:
            resp = self.http.get(get_url(file_name), timeout=1)
        except req.exceptions.ConnectionError:
            return '', 408
            
        return resp.text, resp.status_code
    
    def put(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
            
        headers = dict(request.headers)
        del headers['Authorization']
        
        try:
            resp = self.http.put(get_url(file_name), data = request.data.decode(), headers = headers, timeout=1)
        except req.exceptions.ConnectionError:
            return '', 408
        return resp.text, resp.status_code
    
    def delete(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
            
        try:
            resp = self.http.delete(get_url(file_name), timeout=1)
        except req.exceptions.ConnectionError:
            return '', 408
            
        return resp.text, resp.status_code
   

@app.route('/auth')
def authorize():
    return balancer.authorize(request)
    
@app.route('/wait', methods=['GET'])
def wait_req():
    return balancer.wait_req()    
    
@app.route('/<file_name>', methods=['GET'])
def get_req(file_name):
    return balancer.get(request, file_name)

@app.route('/<file_name>', methods=['PUT'])
def put_req(file_name):
    return balancer.put(request, file_name)
    
@app.route('/<file_name>', methods=['DELETE'])
def delete_req(file_name):
    return balancer.delete(request, file_name)

if __name__ == '__main__':
    balancer = Balancer()
        
    app.run(host='0.0.0.0', port=os.environ["PORT"])
