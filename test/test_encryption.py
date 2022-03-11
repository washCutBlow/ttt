
import base64
import unittest

from difft.client import DifftClient
from Crypto.Random import get_random_bytes

class TestEncryption(unittest.TestCase):
    def test_encryption(self):
        plaintext = get_random_bytes(64)
        key = get_random_bytes(16)
        client = DifftClient()
        ciphertext, digest = client.encrypt_attachment(plaintext, key)

        decrypted = client.decrypt_attachment(ciphertext, key, digest)
        self.assertEqual(plaintext, decrypted)

