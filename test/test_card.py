from difft import utils
import unittest, time
from difft.attachment import AttachmentBuilder
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APPID = "your app ID"
APPSECRET = "your app secret"

class TestMessage(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_send_msg_to_user(self):
        message = MessageRequestBuilder() \
            .sender("+21112") \
            .to_user(["+70985684427"]) \
            .card(APPID, "1111", "### header") \
            .timestamp_now() \
            .build()
        self.difft_client.send_message(message)
