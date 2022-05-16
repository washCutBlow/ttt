import base64
import hashlib
from time import sleep
import unittest
from difft import utils
import requests, json

from difft.client import DifftClient
from difft.auth import Authenticator
from difft.attachment import AttachmentBuilder
from difft.message import MessageRequestBuilder

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"


class TestAttachment(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_upload_and_download(self):
        attachment = utils.random_str(1024).encode("utf-8")
        uploaded_att = self.difft_client.upload_attachment("+60000", [], ["+76459652574", "+60000"], attachment)
        # frequency limit
        sleep(1)
        uploaded_att_twice = self.difft_client.upload_attachment("+60000", [], ["+76459652574", "+60000"], attachment)
        self.assertEqual(uploaded_att.get("cipherHash"), uploaded_att_twice.get("cipherHash"))

        self.assertEqual(uploaded_att.get("fileSize"), len(attachment))

        downloaded_att = self.difft_client.download_attachment("+60000", uploaded_att.get("key"),
                                                               uploaded_att.get("authorizeId"),
                                                               uploaded_att.get("cipherHash"))
        self.assertEqual(attachment, downloaded_att)

        # frequency limit
        sleep(1)
        downloaded_att_twice = self.difft_client.download_attachment("+60000", uploaded_att_twice.get("key"),
                                                                     uploaded_att_twice.get("authorizeId"),
                                                                     uploaded_att_twice.get("cipherHash"))
        self.assertEqual(attachment, downloaded_att_twice)

        self.assertEqual(downloaded_att, downloaded_att_twice)

    def test_send_attachment(self):
        my_auth = Authenticator(appid=APPID, key=APPSECRET.encode("utf-8"))
        attachment = utils.random_str(1024).encode("utf-8")
        uploaded_att = self.difft_client.upload_attachment("+60000", [], ["+76459652574", "+75853524385"], attachment)

        # 发送消息
        msg_attachment = {
            "contentType": "text/html",
            "authorizeId": uploaded_att.get("authorizeId"),
            "key": uploaded_att.get("key"),
            "size": uploaded_att.get("fileSize"),
            "fileName": "test.txt",
            "digest": uploaded_att.get("cipherHash")
        }
        body = {"version": 1, "src": "+60000", "dest": {"wuid": ["+76459652574", "+75853524385"], "type": "USER"},
                "type": "TEXT", "timestamp": utils.current_milli_time(),
                "msg": {"body": "test", "attachment": msg_attachment}}
        url = "https://openapi.test.difft.org/v1/messages"
        resp = requests.post(url=url, json=body, auth=my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

    def test_append_auth(self):
        my_auth = Authenticator(appid=APPID, key=APPSECRET.encode("utf-8"))
        attachment = utils.random_str(1024).encode("utf-8")
        uploaded_att = self.difft_client.upload_attachment("+60000", [], ["+75853524385"], attachment)

        # 发送消息
        msg_attachment = {
            "contentType": "text/html",
            "authorizeId": uploaded_att.get("authorizeId"),
            "key": uploaded_att.get("key"),
            "size": uploaded_att.get("fileSize"),
            "fileName": "test.txt",
            "digest": uploaded_att.get("cipherHash")
        }
        # user +76459652574 don't have authorization yet
        body = {"version": 1, "src": "+60000", "dest": {"wuid": ["+76459652574"], "type": "USER"}, "type": "TEXT",
                "timestamp": utils.current_milli_time(), "msg": {"body": "test", "attachment": msg_attachment}}
        url = "https://openapi.test.difft.org/v1/messages"
        resp = requests.post(url=url, json=body, auth=my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

        # append auth to user +76459652574 
        key_byte = base64.b64decode(uploaded_att.get("key"))
        fileHash = hashlib.sha256(key_byte).digest()
        new_authorizeId = self.difft_client.append_attachment_authorization("+60000",
                                                                            base64.b64encode(fileHash).decode("utf-8"),
                                                                            uploaded_att.get("fileSize"), [],
                                                                            ["+76459652574"])

        # re-send the msg with new authorize id
        msg_attachment["authorizeId"] = new_authorizeId
        body = {"version": 1, "src": "+60000", "dest": {"wuid": ["+76459652574"], "type": "USER"}, "type": "TEXT",
                "timestamp": utils.current_milli_time(), "msg": {"body": "test", "attachment": msg_attachment}}
        url = "https://openapi.test.difft.org/v1/messages"
        resp = requests.post(url=url, json=body, auth=my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

        self.difft_client.delete_attachment_authorization("+60000", base64.b64encode(fileHash).decode("utf-8"),
                                                          [new_authorizeId])

        # re-send msg with the same authorize id, should not have authorize
        body = {"version": 1, "src": "+60000", "dest": {"wuid": ["+76459652574"], "type": "USER"}, "type": "TEXT",
                "timestamp": utils.current_milli_time(), "msg": {"body": "test", "attachment": msg_attachment}}
        resp = requests.post(url=url, json=body, auth=my_auth)
        data = json.loads(resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data.get("status", -1), 0)

    def test_upload_file(self):
        with open("attachment.txt", "r") as f:
            plaintext = f.read()
        plaintext = plaintext.encode("utf-8")
        uploaded_attachment = self.difft_client.upload_attachment("+60000", [], ["+76459652574"], plaintext)
        attachment = AttachmentBuilder() \
            .authorize_id(uploaded_attachment.get("authorizeId")) \
            .key(uploaded_attachment.get("key")) \
            .file_size(uploaded_attachment.get("fileSize")) \
            .file_name("test.txt") \
            .digest(uploaded_attachment.get("cipherHash")) \
            .build()
        message = MessageRequestBuilder() \
            .sender("+60000") \
            .to_user(["+76459652574"])\
            .message("hello, this is a test message") \
            .attachment(attachment) \
            .timestamp_now() \
            .build()
        self.difft_client.send_message(message)