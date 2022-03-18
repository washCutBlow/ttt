import unittest, time
from difft import utils
from difft.attachment import AttachmentBuilder
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"


class TestMessage(unittest.TestCase):
    difft_client = DifftClient(APPID, APPSECRET)

    def test_send_msg_to_user(self):
        # frequency limit
        time.sleep(1)
        message = MessageRequestBuilder() \
            .sender("+60000") \
            .to_user(["+76459652574"]) \
            .message("hello, this is a test message") \
            .build()
        self.difft_client.send_message(message)

    def test_send_msg_to_group(self):
        # frequency limit
        time.sleep(1)
        message = MessageRequestBuilder() \
            .sender("+60000") \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7") \
            .message("hello, this is a test message") \
            .at_user(["+76459652574"]) \
            .build()
        self.difft_client.send_message(message)

    def test_send_attachment(self):
        plain_attachment = utils.random_str(1024).encode("utf-8")
        uploaded_attachment = self.difft_client.upload_attachment("+60000", [], ["+76459652574"], plain_attachment)

        attachment = AttachmentBuilder() \
            .authorize_id(uploaded_attachment.get("authorizeId")) \
            .key(uploaded_attachment.get("key")) \
            .file_size(uploaded_attachment.get("fileSize")) \
            .file_name("test.txt") \
            .digest(uploaded_attachment.get("cipherHash")) \
            .build()

        # frequency limit
        time.sleep(1)
        message = MessageRequestBuilder() \
            .sender("+60000") \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7") \
            .message("hello, this is a test message") \
            .at_user(["+76459652574"]) \
            .attachment(attachment) \
            .timestamp_now() \
            .build()
        self.difft_client.send_message(message)
