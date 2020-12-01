#!/usr/bin/env python3
from flask import Flask, request
import requests as req
import base64
import json
import jwt
import os

app = Flask(__name__)

class Balancer:
    
    def __init__(self):
        self.users = {'killer':'qwerty123', 'vasya':'123'}
        self.usr_tokens = {}
    
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
            
    def get(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
        resp = req.get('http://{0}:{1}/storage/{2}'.format(f'pm-default-server-container-{str(hash(file_name)%2 + 1)}', os.environ["PORT"] + hash(file_name)%2 + 1, file_name))
        return resp.text, resp.status_code
    
    def put(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
        resp = req.put('http://{0}:{1}/storage/{2}'.format(f'pm-default-server-container-{str(hash(file_name)%2 + 1)}', os.environ["PORT"] + hash(file_name)%2 + 1, file_name) , data = request.data.decode(), headers = request.headers)
        return resp.text, resp.status_code
    
    def delete(self, request, file_name):
        try:
            self.check_JWT_auth(request.headers.get('Authorization').split(' ')[1])
        except:
            return '', 403
        resp = req.delete('http://{0}:{1}/storage/{2}'.format(f'pm-default-server-container-{str(hash(file_name)%2 + 1)}', os.environ["PORT"] + hash(file_name)%2 + 1, file_name))
        return resp.text, resp.status_code
   

@app.route('/auth')
def authorize():
    return balancer.authorize(request)
    
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
