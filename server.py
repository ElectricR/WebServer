#!/usr/bin/env python3
from flask import Flask, request

import controller
import service
import os

app = Flask(__name__)

@app.route('/storage/<file_name>', methods=['GET'])
def get_req(file_name):
    resp = serv.get(file_name)
    if resp == None:
        return '', 404
    else:
        return resp, 200

@app.route('/storage/<file_name>', methods=['PUT'])
def put_req(file_name):
    if not ctrl.validate(request):
    	return '', 400
    serv.put(file_name, request.data.decode())
    return '', 201
    
@app.route('/storage/<file_name>', methods=['DELETE'])
def delete_req(file_name):
    serv.delete(file_name)
    return '', 204

if __name__ == '__main__':
    ctrl = controller.Controller()
    serv = service.Service()
    
    app.run(host='0.0.0.0', port=os.environ["PORT"])
