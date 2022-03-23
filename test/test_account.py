import unittest, time
from difft import utils
from difft.attachment import AttachmentBuilder
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"


class TestMessage(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_get_account(self):
        res = self.difft_client.get_account({"email": "ian.p@binance.com"})
        print(res)

        res = self.difft_client.get_account_by_email("ian.p@binance.com")
        print(res)

        res = self.difft_client.get_account_by_wuid("+60000")
        print(res)
