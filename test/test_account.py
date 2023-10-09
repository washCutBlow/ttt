import unittest
from difft.client import DifftClient

APPID = "your app ID"
APPSECRET = "your app secret"


class TestAccount(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_get_account(self):
        res = self.difft_client.get_account({"email": "bob@domain.com"})
        print(res)

        res = self.difft_client.get_account_by_email("bob@domain.com")
        print(res)

        res = self.difft_client.get_account_by_wuid("+60000")
        print(res)
