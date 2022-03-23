import base64
import hashlib
import hmac
import json
import logging
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from difft import constants
from difft.auth import Authenticator


class DifftClient:
    BLOCK_SIZE = 16

    def __init__(self, appid: str, key: str, host: str = "https://openapi.test.difft.org"):
        self._auth = Authenticator(appid, key.encode("utf-8"))
        self._host = host

    def upload_attachment(self, send_wuid: str, group_ids: list, acceptor_wuid: list, attachment: bytes) -> dict:
        """
        Upload attachment to oss storage
        :param send_wuid: bot wuid
        :param group_ids: list of group id
        :param acceptor_wuid: list of acceptor wuid
        :param attachment: bytes of attachment
        :return: map of authorizeId, key, cipherHash, fileSize
        """
        key = hashlib.sha512(attachment).digest()
        fileHash = hashlib.sha256(key).digest()
        fileSize = len(attachment)
        is_exist_body = dict(wuid=send_wuid, fileHash=base64.b64encode(fileHash).decode("utf-8"), fileSize=fileSize,
                             gids=group_ids, numbers=acceptor_wuid)
        is_exist_resp = requests.post(url=self._host + constants.URL_ISEXIST, json=is_exist_body, auth=self._auth)

        is_exist_resp_obj = json.loads(is_exist_resp.text)
        if is_exist_resp_obj.get("status") != 0:
            raise Exception(is_exist_resp_obj.get("reason"))

        data = is_exist_resp_obj.get("data")
        if data.get("exists"):
            # file already exist, skip upload
            return dict(
                authorizeId=data.get("authorizeId"),
                key=base64.b64encode(key).decode("utf-8"),
                cipherHash=data.get("cipherHash"),
                fileSize=fileSize
            )

        # upload attachment to oss
        ciphertext = self.encrypt_attachment(attachment, key)
        cipherHash = hashlib.md5(ciphertext).hexdigest()
        requests.put(data.get("url"), data=ciphertext)

        upload_info = dict(
            wuid=send_wuid,
            fileHash=base64.b64encode(fileHash).decode("utf-8"),
            attachmentId=data.get("attachmentId"),
            fileSize=fileSize,
            hashAlg="SHA256",
            keyAlg="SHA512",
            encAlg="AES-CBC-SHA256",
            cipherHash=cipherHash,
            cipherHashType="MD5",
            gids=group_ids,
            numbers=acceptor_wuid,
        )
        # report uploadinfo to server
        upload_info_resp = requests.post(url=self._host + constants.URL_UPLOAD_ATTACHMENT, json=upload_info,
                                         auth=self._auth)
        upload_info_resp_obj = json.loads(upload_info_resp.text)
        if upload_info_resp_obj.get("status") != 0:
            raise Exception(upload_info_resp_obj.get("reason"))
        data = upload_info_resp_obj.get("data")
        return dict(
            authorizeId=data.get("authorizeId"),
            key=base64.b64encode(key).decode("utf-8"),
            cipherHash=cipherHash,
            fileSize=fileSize
        )

    def download_attachment(self, wuid, key, authorize_id, cipher_hash, url=None) -> bytes:
        """
        Download attachment from oss
        :param wuid: bot id
        :param key:
        :param authorize_id:
        :param cipher_hash:
        :param url: attachment download link if existed, default None
        :return: plain attachment, bytes
        """
        key = base64.b64decode(key)
        if not url:
            fileHash = hashlib.sha256(key).digest()
            download_attachment_body = dict(wuid=wuid, fileHash=base64.b64encode(fileHash).decode("utf-8"),
                                            authorizeId=authorize_id)
            download_attachment_resp = requests.post(url=self._host + constants.URL_DOWNLOAD_ATTACHMENT,
                                                     json=download_attachment_body, auth=self._auth)
            download_attachment_obj = json.loads(download_attachment_resp.text)
            if download_attachment_obj.get("status") != 0:
                raise Exception(download_attachment_obj.get("reason"))
            data = download_attachment_obj.get("data")
            url = data.get("url")
        attachment_resp = requests.get(url=url)
        attachment = attachment_resp.content
        return self.decrypt_attachment(attachment, key, bytes.fromhex(cipher_hash))

    def append_attachment_authorization(self, wuid, fil_hash, file_size, group_ids, acceptor_wuid):
        """
        Append user authorization to existed attachment
        :param wuid: bot id
        :param fil_hash:
        :param file_size:
        :param group_ids:
        :param acceptor_wuid:
        :return: authorizeId if success, otherwise raise exception
        """
        is_exist_body = dict(wuid=wuid, fileHash=fil_hash, fileSize=file_size, gids=group_ids, numbers=acceptor_wuid)
        is_exist_resp = requests.post(url=self._host + constants.URL_ISEXIST, json=is_exist_body, auth=self._auth)
        is_exist_resp_obj = json.loads(is_exist_resp.text)
        if is_exist_resp_obj.get("status") != 0:
            raise Exception(is_exist_resp_obj.get("reason"))

        data = is_exist_resp_obj.get("data")
        if not data.get("exists"):
            raise Exception("file not exist")

        return data.get("authorizeId")

    def delete_attachment_authorization(self, wuid, filehash, authorizeIds):
        """
        Delete specific authorization by authorizeIds
        :param wuid:
        :param filehash:
        :param authorizeIds:
        :return: True if success
        """
        delete_attachment_auth_body = dict(wuid=wuid,
                                           delAuthorizeInfos=[dict(fileHash=filehash, authorizeIds=authorizeIds)])
        delete_attachment_auth_resp = requests.post(url=self._host + constants.URL_DEL_ATTACHMENT,
                                                    json=delete_attachment_auth_body, auth=self._auth)
        delete_attachment_auth_obj = json.loads(delete_attachment_auth_resp.text)
        if delete_attachment_auth_obj.get("status") != 0:
            logging.error(delete_attachment_auth_obj.get("reason"))
            return False
        return True

    def send_message(self, msg):
        """
        Send message
        :param msg: MessageRequest
        :return: list of fail reason, 
                [{ 
                "wuid":"idxxx", 
                "groupID":"{wea group id}",
                "reason":"failed reason"
                }]
        """
        send_msg_resp = requests.post(url=self._host + constants.URL_SEND_MSG, json=msg, auth=self._auth)
        if send_msg_resp.status_code != 200:
            raise Exception("server response %d" % send_msg_resp.status_code)
        send_msg_resp_obj = json.loads(send_msg_resp.text)
        if send_msg_resp_obj.get("status") != 0:
            raise Exception("send message failed", send_msg_resp_obj.get("errors"), send_msg_resp_obj.get("error"))
        return send_msg_resp_obj.get("errors")

    def get_account_by_email(self, email):
        param = dict(email=email)
        return self.get_account(param)

    def get_account_by_wuid(self, wuid):
        param = dict(wuid=wuid)
        return self.get_account(param)

    def get_account(self, params):
        resp = requests.get(url=self._host + constants.URL_ACCOUNT, params=params, auth=self._auth)
        if resp.status_code != 200:
            raise Exception("server response error, code", resp.status_code)
        resp_obj = json.loads(resp.text)
        if resp_obj.get("status") != 0:
            raise Exception(resp_obj.get("reason"))
        return resp_obj.get("data")

    def encrypt_attachment(self, attachment, key):
        if len(key) != 64:
            raise Exception("got invalid length keys (%d bytes)" % len(key))

        iv = get_random_bytes(16)
        cipher = AES.new(key[:32], AES.MODE_CBC, iv)
        attachment_cipher = cipher.encrypt(self.pkcs5_pad(attachment))
        mac = self.hmac_sha256(key[32:], iv, attachment_cipher)
        ciphertext = iv + attachment_cipher + mac

        return ciphertext

    def decrypt_attachment(self, ciphertext, keys, thier_digest) -> bytes:
        if len(keys) != 64:
            raise Exception("got invalid length keys")

        ciphertext_length = len(ciphertext)
        iv = ciphertext[:16]
        mac = ciphertext[ciphertext_length - 32:]
        attachment_cipher = ciphertext[16:ciphertext_length - 32]
        calculated_mac = self.hmac_sha256(keys[32:], iv, attachment_cipher)
        if mac != calculated_mac:
            raise Exception("bad mac")
        if len(thier_digest) != 16:
            raise Exception("unknown digest")
        calculated_digest = hashlib.md5(ciphertext).digest()
        if calculated_digest != thier_digest:
            raise Exception("digest not match")

        cipher = AES.new(keys[:32], AES.MODE_CBC, iv)
        attachment_cipher = cipher.decrypt(attachment_cipher)
        return self.pkcs5_unpad(attachment_cipher)

    def pkcs5_pad(self, s):
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

    def pkcs5_unpad(self, s):
        """
        unpadding according to PKCS #5
        @param s: string to unpad
        @type s: string
        @rtype: string
        """
        return s[0:-s[-1]]

    def hmac_sha256(self, keys, iv, ciphertext):
        digest = hmac.new(keys, iv + ciphertext, hashlib.sha256).digest()
        return digest
