import requests
import unittest
import json

from difft.auth import Authenticator
from difft.utils import *

APPID = "your app ID"
APPSECRET = "your app secret"


class TestSign(unittest.TestCase):
    my_auth = Authenticator(appid=APPID, key=APPSECRET.encode("utf-8"))

    # def test_account(self):
    # """
    # 创建账号
    # """
    # puid = random_str(10)
    # body = {"puid":puid, "nickname":"python-sdk-test"}
    # url = "https://openapi.test.difft.org/v1/accounts"

    # resp = requests.post(url=url, json=body, auth=self.my_auth)
    # data_create = json.loads(resp.text)
    # self.assertEqual(resp.status_code, 200)
    # self.assertEqual(data_create.get("status", -1), 0)

    # """
    # 查询账户
    # """
    # url =  "https://openapi.test.difft.org/v1/accounts?wuid=" + data_create.get("data").get("wuid")
    # resp = requests.get(url=url, auth=self.my_auth)
    # data_query = json.loads(resp.text)
    # self.assertEqual(resp.status_code, 200)
    # self.assertEqual(data_query.get("status", -1), 0)

    # """
    # 更新账户
    # """
    # body = {"wuid": data_create.get("data").get("wuid"), "nickname": "python-sdk-test-update"}
    # url =  "https://openapi.test.difft.org/v1/accounts"
    # resp = requests.put(url=url, json=body,auth=self.my_auth)
    # data_update = json.loads(resp.text)
    # self.assertEqual(resp.status_code, 200)
    # self.assertEqual(data_update.get("status", -1), 0)

    # def test_group(self):
    # """
    # 创建组
    # """
    # body = {"operator": "+85533430156", "name": "python sdk test group", "accounts":["+74708405548"],"invitationRule":2}
    # url = "https://openapi.test.difft.org/v1/groups"
    # resp = requests.post(url=url, json=body, auth=self.my_auth)
    # data = json.loads(resp.text)
    # self.assertEqual(resp.status_code, 200)
    # self.assertEqual(data.get("status", -1), 0)

    # """查询groups"""
    # url = "https://openapi.test.difft.org/v1/groups?operator=%2B21013"
    # resp = requests.get(url=url, auth=self.my_auth)
    # data = json.loads(resp.text)
    # self.assertEqual(resp.status_code, 200)
    # self.assertEqual(data.get("status", -1), 0)

    # def test_send_message(self):
    #     """
    #     发送消息
    #     """
    #     body = {"version": 1,"src": "+85533430156","dest": { "wuid": ["+74708405548"],"type": "USER"},"type": "TEXT","timestamp": current_milli_time(),"msg": {"body": "test"}}
    #     url = "https://openapi.test.difft.org/v1/messages"
    #     resp = requests.post(url=url, json=body, auth=self.my_auth)
    #     data = json.loads(resp.text)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(data.get("status", -1), 0)

    # def test_team(self):
    #     """"
    #     创建team
    #     """

    #     body = {"name": "python sdk test " + random_str(5)}
    #     url = "https://openapi.test.difft.org/v1/teams"
    #     resp = requests.post(url=url, json=body, auth=self.my_auth)
    #     data = json.loads(resp.text)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(data.get("status", -1), [0, 8]) # status 8: team exist

    def test_file(self):
        """
        文件是否存在
        """
        body = {"wuid": "+60000", "fileHash": "3VyVsXrGkZ8EzFlhCGq/RfPXsJfxxHWChPhixKaOYO4=", "fileSize": 1024,
                "gids": [], "numbers": ["+76459652574", "+75853524385"]}
        url = "https://openapi.test.difft.org/v1/file/isExists"
        resp = requests.post(url=url, json=body, auth=self.my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)  # file no permission

    def test_oauth_user_info(self):
        url = "https://openapi.test.difft.org/v1/oauth/getUserInfo"
        resp = requests.get(url=url, params={"columns": "name,email"}, headers={"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJ1aWQiOiIrNzIyNDA1NDM5MDMiLCJ2ZXIiOjEsImFwcGlkIjoiYTE0Y2EwMzljNjY3MTc5Y2RjIiwic2NvcGUiOlsiTmFtZVJlYWQiLCJFbWFpbFJlYWQiXSwiZXhwIjoxNjYwMDM4OTQ0LCJpYXQiOjE2NTk5NTI1NDQsImRpZCI6MX0.Af3AJ6ugGTj26VzqMefZJg-vdNoNjiMQHw8Fi8EvR1HmFbCUO8FgKJ1EpoWjMVRrQBggrfxr7iw51lGZU6YnB16hAOww5IgziiehdWRMjmmy9vja8iK7OCEq1TXGttghwzKtrqaXRTu1v00o_M65vaMNkFE9XOzHelA2pmUTvxxHqeOZ"},auth=self.my_auth)
        print(resp.text)