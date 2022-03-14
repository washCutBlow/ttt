
from difflib import diff_bytes
import unittest
from difft import utils
import requests, json

from difft.client import DifftClient
from difft.auth import Authenticator


class TestAttachment(unittest.TestCase):
    difft_client = DifftClient("f250845b274f4a5c01", "w0m6nTOIIspxR0wmGJbEvAOfNnyf")
    def test_upload_and_download(self):
        attachment = utils.random_str(1024).encode("utf-8")
        uploaded_att = self.difft_client.upload_attachment("+60000", [], ["+76459652574"], attachment) 
        uploaded_att_twice = self.difft_client.upload_attachment("+14253628872", [], ["+14253628872"], attachment) 
        self.assertEqual(uploaded_att.get("cipherHash"), uploaded_att_twice.get("cipherHash"))

        self.assertEqual(uploaded_att.get("fileSize"), len(attachment))

        downloaded_att = self.difft_client.download_attachment("+14253628872", uploaded_att.get("key"), uploaded_att.get("authorizeId"), uploaded_att.get("cipherHash"))
        self.assertEqual(attachment, downloaded_att)
        
        downloaded_att_twice = self.difft_client.download_attachment("+14253628872", uploaded_att_twice.get("key"), uploaded_att_twice.get("authorizeId"), uploaded_att_twice.get("cipherHash"))
        self.assertEqual(attachment, downloaded_att_twice)

        self.assertEqual(downloaded_att, downloaded_att_twice)
    
    def test_send_attachment(self):
        my_auth = Authenticator(appid="f250845b274f4a5c01", key="w0m6nTOIIspxR0wmGJbEvAOfNnyf".encode("utf-8"))
        attachment = utils.random_str(1024).encode("utf-8")
        uploaded_att = self.difft_client.upload_attachment("+60000", [], ["+76459652574", "+75853524385"], attachment) 
        print("upload resp:", uploaded_att)

        # 发送消息
        msg_attachment = {
            "contentType": "text/html",
            "authorizeId": uploaded_att.get("authorizeId"),
            "key": uploaded_att.get("key"), 
            "size": uploaded_att.get("fileSize"),
            "fileName": "test.txt",
            "digest": uploaded_att.get("cipherHash")
            }
        body = {"version": 1,"src": "+60000","dest": { "wuid": ["+76459652574", "+75853524385"],"type": "USER"},"type": "TEXT","timestamp": utils.current_milli_time(),"msg": {"body": "test","attachment": msg_attachment}}
        print("msg:", body)
        url = "https://openapi.test.difft.org/v1/messages"
        resp = requests.post(url=url, json=body, auth=my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)


