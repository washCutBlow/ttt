from enum import auto
import requests
import unittest
import json

from src.authenticator import Authenticator
from src.utils import *

class TestSign(unittest.TestCase):

    my_auth = Authenticator(appid="06d4bdffbfaeef75a52e", key="KyYfHvRUpVr9NlLSVUZTOE6VPLQd".encode("utf-8"))

    def test_account(self):
        """
        创建账号
        """
        puid = random_str(10)
        body = {"puid":puid, "nickname":"python-sdk-test"}
        url = "https://openapi.test.difft.org/v1/accounts"

        resp = requests.post(url=url, json=body, auth=self.my_auth)
        data_create = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data_create.get("status", -1), 0)

        """
        查询账户
        """
        url =  "https://openapi.test.difft.org/v1/accounts?wuid=" + data_create.get("data").get("wuid")
        resp = requests.get(url=url, auth=self.my_auth)
        data_query = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data_query.get("status", -1), 0)

        """
        更新账户
        """
        body = {"wuid": data_create.get("data").get("wuid"), "nickname": "python-sdk-test-update"}
        url =  "https://openapi.test.difft.org/v1/accounts"
        resp = requests.put(url=url, json=body,auth=self.my_auth)
        data_update = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data_update.get("status", -1), 0)

    
    def test__group(self):
        """
        创建组
        """
        body = {"operator": "+85533430156", "name": "python sdk test group", "accounts":["+74708405548"],"invitationRule":2}
        url = "https://openapi.test.difft.org/v1/groups"
        resp = requests.post(url=url, json=body, auth=self.my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

    def test_send_message(self):
        """
        发送消息
        """
        body = {"version": 1,"src": "+85533430156","dest": { "wuid": ["+74708405548"],"type": "USER"},"type": "TEXT","timestamp": 1646105966000,"msg": {"body": "test"}}
        url = "https://openapi.test.difft.org/v1/messages"
        resp = requests.post(url=url, json=body, auth=self.my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)
        

    def test_team(self):
        """"
        创建team
        """
        
        body = {"name": "python sdk test " + random_str(5)}
        url = "https://openapi.test.difft.org/v1/teams"
        resp = requests.post(url=url, json=body, auth=self.my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(data.get("status", -1), [0, 8]) # status 8: team exist
    
    def test_file(self):
        """
        文件是否存在
        """
        body = {"wuid": "123123", "fileHash": "1123", "fileSize": 100, "gids": ["1", "2"], "numbers": ["1", "2"]}
        url = "https://openapi.test.difft.org/v1/file/isExists"
        resp = requests.post(url=url, json=body, auth=self.my_auth)
        print(resp.text)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

if __name__ == '__main__':
    unittest.main()