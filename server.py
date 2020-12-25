#!/usr/bin/env python3
from flask import Flask, request
from repository import DBase, Cache
from controller import Controller
from service import Service
import os


app = Flask(__name__)


@app.route('/wait', methods=['GET'])
def wait_req():
    return controller.handle_wait()


@app.route('/storage/<file_name>', methods=['GET'])
def get_req(file_name):
    return controller.handle_get(file_name)


@app.route('/storage/<file_name>', methods=['PUT'])
def put_req(file_name):
    return controller.handle_put(request, file_name, request.data.decode())


@app.route('/storage/<file_name>', methods=['DELETE'])
def delete_req(file_name):
    return controller.handle_delete(file_name)


if __name__ == '__main__':
    controller = Controller(Service(Cache(
        os.environ['REDIS_HOST'], os.environ['REDIS_PORT']),
        DBase(int(os.environ['DATABASE_PORT']))))

    app.run(host='0.0.0.0', port=os.environ["PORT"])
