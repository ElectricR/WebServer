import unittest
import os
import requests as req
import dotenv
from time import sleep

def put_req(file_, data):
    return req.put(f'http://localhost:{os.environ["PORT"]}/{file_}', data=data, headers={'Content-Type':'application/json'})

def get_req(file_):
    return req.get(f'http://localhost:{os.environ["PORT"]}/{file_}')

def delete_req(file_):
    return req.delete(f'http://localhost:{os.environ["PORT"]}/{file_}')

class test_server(unittest.TestCase):

    def setUp(self):
        dotenv.load_dotenv()
        os.system("make start")
        sleep(3)

    def test_normal(self):
        self.assertEqual(put_req("file1", "{1:2}").status_code, 201)
        self.assertEqual(put_req("file2", '{"Alice":"Bob"}').status_code, 201)
        self.assertEqual(put_req("file3", '').status_code, 201)
        r = get_req("file3")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '')
        r = get_req("file2")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '{"Alice":"Bob"}')
        r = get_req("file1")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '{1:2}')
        r = get_req("file4")
        self.assertEqual(r.status_code, 404)
        r = delete_req("file4")
        self.assertEqual(r.status_code, 204)
        self.assertEqual(put_req("file1", "{5:2}").status_code, 201)
        self.assertEqual(get_req("file1").text, "{5:2}")
        self.assertEqual(delete_req("file1").status_code, 204)
        self.assertEqual(delete_req("file2").status_code, 204)
        self.assertEqual(delete_req("file3").status_code, 204)
        self.assertEqual(delete_req("file4").status_code, 204)
        self.assertEqual(get_req("file1").status_code, 404)
        self.assertEqual(get_req("file2").status_code, 404)
        self.assertEqual(get_req("file3").status_code, 404)
        

    def tearDown(self):
        os.system("make stop")

if __name__ == '__main__':
    unittest.main()
