import unittest
import os
import requests as req
import dotenv
import base64
from time import sleep

def put_req(file_, data, token = None):
    headers = {'Content-Type':'application/json'}
    if token: headers['Authorization'] = f'Bearer {token}'
    return req.put(f'http://localhost:{os.environ["PORT"]}/{file_}', data=data, headers=headers)

def get_req(file_, token = None):
    headers = {}
    if token: headers['Authorization'] = f'Bearer {token}'
    return req.get(f'http://localhost:{os.environ["PORT"]}/{file_}', headers=headers)

def delete_req(file_, token = None):
    headers = {}
    if token: headers['Authorization'] = f'Bearer {token}'
    return req.delete(f'http://localhost:{os.environ["PORT"]}/{file_}', headers=headers)

def auth(login, password):
    headers = {'Authorization': "Basic " + base64.standard_b64encode(f'{login}:{password}'.encode()).decode()}
    return req.get(f'http://localhost:{os.environ["PORT"]}/auth', headers = headers)

class integration_test(unittest.TestCase):

    def setUp(self):
        dotenv.load_dotenv()
        os.system("docker-compose -f compose.yaml --env-file .env up -d")
        sleep(1)
        self.killer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoia2lsbGVyIiwicm9sZSI6IndyaXRlIn0.DTHlSwBvmPn7soPbSlZn4vn28Z6r1EhC_kgE-0_lxzs"

    def test_authorization(self):
        self.assertEqual(auth('killer', 'qwerty12').status_code, 401)
        self.assertEqual(auth('vasya', 'qwerty123').status_code, 401)
        self.assertEqual(auth('sunshine', 'asd').status_code, 401)
        
        self.assertEqual(get_req("file1").status_code, 403)
        self.assertEqual(put_req("file1", "{1:2}").status_code, 403)
        
        resp = auth('killer', 'qwerty123')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, self.killer_token)
    
    def test_get_nonexistent_files(self):
        auth('killer', 'qwerty123')
        self.assertEqual(get_req("file1", self.killer_token).status_code, 404)
        self.assertEqual(get_req("file2", self.killer_token).status_code, 404)
        self.assertEqual(get_req("file3", self.killer_token).status_code, 404)
        self.assertEqual(get_req("file4", self.killer_token).status_code, 404)
        
    def test_deletion(self):
        auth('killer', 'qwerty123')
        self.assertEqual(put_req("file1", "{1:2}", token=self.killer_token).status_code, 201)
        self.assertEqual(put_req("file2", '{"Alice":"Bob"}', token=self.killer_token).status_code, 201)
        
        self.assertEqual(get_req("file1", token=self.killer_token).text, "{1:2}")
        self.assertEqual(delete_req("file1", token=self.killer_token).status_code, 204)
        self.assertEqual(get_req("file1", token=self.killer_token).status_code, 404)
        self.assertEqual(delete_req("file1", token=self.killer_token).status_code, 204)
        
        self.assertEqual(get_req("file2", token=self.killer_token).text, '{"Alice":"Bob"}')
        self.assertEqual(delete_req("file2", token=self.killer_token).status_code, 204)
        self.assertEqual(get_req("file2", token=self.killer_token).status_code, 404)
    
    def test_rewrite_put(self):
        auth('killer', 'qwerty123')
        self.assertEqual(put_req("file1", "{1:2}", token=self.killer_token).status_code, 201)
        self.assertEqual(get_req("file1", token=self.killer_token).text, "{1:2}")
        
        self.assertEqual(put_req("file1", "{2:1}", token=self.killer_token).status_code, 201)
        self.assertEqual(get_req("file1", token=self.killer_token).text, "{2:1}")
        
        self.assertEqual(put_req("file1", '{"Apple":"Orange"}', token=self.killer_token).status_code, 201)
        self.assertEqual(get_req("file1", token=self.killer_token).text, '{"Apple":"Orange"}')
        
        self.assertEqual(put_req("file1", '{"Apple":100}', token=self.killer_token).status_code, 201)
        self.assertEqual(get_req("file1", token=self.killer_token).text, '{"Apple":100}')  
        
        self.assertEqual(delete_req("file1", token=self.killer_token).status_code, 204)  
        self.assertEqual(get_req("file1", token=self.killer_token).status_code, 404)   

    def tearDown(self):
        os.system("make stop")

if __name__ == '__main__':
    unittest.main()
