import unittest
from difft.client import DifftClient

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"


class TestAccount(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_get_account(self):
        res = self.difft_client.get_account({"email": "ian.p@binance.com"})
        print(res)

        res = self.difft_client.get_account_by_email("ian.p@binance.com")
        print(res)

        res = self.difft_client.get_account_by_wuid("+60000")
        print(res)
