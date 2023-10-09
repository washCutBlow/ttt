import time
import unittest
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APPID = "your app ID"
APPSECRET = "your app secret"


class TestRecall(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_send_msg_to_user(self):
        message = MessageRequestBuilder() \
            .sender("+60000") \
            .to_user(["+76459652574"]) \
            .card(APPID, "1111", "### header") \
            .timestamp_now() \
            .build()
        self.difft_client.send_message(message)

        # wait for 10s and then recall the message
        time.sleep(10)

        recall_msg = MessageRequestBuilder() \
            .sender("+60000") \
            .to_user(["+76459652574"]) \
            .recall("+60000", message.get("timestamp")) \
            .timestamp_now() \
            .build()
        self.difft_client.send_message(recall_msg)
