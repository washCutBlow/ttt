import hashlib
import hmac
from logging import exception
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class DifftClient:

    BLOCK_SIZE = 32

    def __init__(self):
        pass
        
    def encrypt_attachment(self, attachment, key):
        if len(key) != 16:
            raise Exception("got invalid length keys (%d bytes)" % len(key))
        
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        attachment_cipher = cipher.encrypt(self.pkcs5_pad(attachment))
        mac = self.hmac_sha256(key[32:], iv, attachment_cipher)
        digest = hashlib.md5(iv+attachment_cipher+mac).digest()

        ciphertext = iv + attachment_cipher + mac

        return ciphertext, digest

    def decrypt_attachment(self, ciphertext, keys, thier_digest):
        if len(keys) != 16:
            raise Exception("got invalid length keys")
        
        ciphertext_length = len(ciphertext)
        iv = ciphertext[:16]
        mac = ciphertext[ciphertext_length-32:]
        attachment_cipher = ciphertext[16:ciphertext_length-32]
        calculated_mac = self.hmac_sha256(keys[32:], iv, attachment_cipher)
        if mac != calculated_mac:
            raise Exception("bad mac")
        if len(thier_digest) != 16:
            raise Exception("unknown digest")
        calculated_digest = hashlib.md5(ciphertext).digest()
        if calculated_digest != thier_digest:
            raise Exception("digest not match")

        cipher = AES.new(keys, AES.MODE_CBC, iv)
        attachment_cipher = cipher.decrypt(attachment_cipher)
        return self.pkcs5_unpad(attachment_cipher)


    def pkcs5_pad(self,s):
        """
        padding to blocksize according to PKCS #5
        calculates the number of missing chars to BLOCK_SIZE and pads with
        ord(number of missing chars)
        @param s: string to pad
        @type s: string
        @rtype: string
        """
        padded = self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE
        return s + padded * chr(padded).encode("utf-8")
        

    def pkcs5_unpad(self,s):
        """
        unpadding according to PKCS #5
        @param s: string to unpad
        @type s: string
        @rtype: string
        """
        return s[0:-s[-1]]
    
    def hmac_sha256(self, keys, iv, ciphertext):
        digest = hmac.new(keys, iv+ciphertext, hashlib.sha256).digest()
        return digest