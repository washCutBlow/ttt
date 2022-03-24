import unittest
from difft.client import DifftClient

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"


class TestGroup(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_get_group(self):
        res = self.difft_client.get_group_by_botid("+60000")
        print(res)