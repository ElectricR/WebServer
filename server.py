#!/usr/bin/env python3
from flask import Flask, request
import requests as req

import controller


ctrl = controller.Controller()
app = Flask(__name__)

@app.route('/<file_name>', methods=['GET'])
def get_req(file_name):
    resp = req.get('http://{0}:10051/storage/{1}'.format("pm-task9.1-service", file_name))
    return resp.text, resp.status_code

@app.route('/<file_name>', methods=['PUT'])
def put_req(file_name):
    if not ctrl.validate(request):
    	return '', 400
    resp = req.put('http://{0}:10051/storage/{1}'.format("pm-task9.1-service", file_name), data = request.data.decode(), headers = {'Content-Type': 'application/json'})
    return resp.text, resp.status_code
    
@app.route('/<file_name>', methods=['DELETE'])
def delete_req(file_name):
    resp = req.delete('http://{0}:10051/storage/{1}'.format("pm-task9.1-service", file_name))
    return resp.text, resp.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10050)
