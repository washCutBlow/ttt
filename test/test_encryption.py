import base64
import hashlib
import unittest

from difft.client import DifftClient
from Crypto.Random import get_random_bytes

APPID = "your app ID"
APPSECRET = "your app secret"


class TestEncryption(unittest.TestCase):
    def test_encryption(self):
        plaintext = get_random_bytes(64)
        key = get_random_bytes(64)
        client = DifftClient(APPID, APPSECRET)
        ciphertext = client.encrypt_attachment(plaintext, key)
        digest = hashlib.md5(ciphertext).digest()

        decrypted = client.decrypt_attachment(ciphertext, key, digest)
        self.assertEqual(plaintext, decrypted)
