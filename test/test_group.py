import unittest
from difft.client import DifftClient

APPID = "your app ID"
APPSECRET = "your app secret"


class TestGroup(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_get_group(self):
        res = self.difft_client.get_group_by_botid("+60000")
        print(res)
