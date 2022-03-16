import unittest, time

from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"

class TestMessage(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_send_msg_to_user(self):
        # frequency limit
        time.sleep(1)
        message = MessageRequestBuilder()       \
                    .sender("+60000")           \
                    .to_user(["+76459652574"])    \
                    .message("hello, this is a test message") \
                    .build()
        self.difft_client.send_message(message)
    
    def test_send_msg_to_group(self):
        # frequency limit
        time.sleep(1)
        message = MessageRequestBuilder()                           \
                    .sender("+60000")                               \
                    .to_group("a9de6b3ae8c8456d888c4532b487e822")   \
                    .message("hello, this is a test message")       \
                    .at_user(["+76459652574"])                        \
                    .build()
        self.difft_client.send_message(message)