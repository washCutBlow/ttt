import unittest, logging, sys
from difft.client import DifftClient

from difft.difft_ws_listener import DifftWsListener
from difft.message import MessageRequestBuilder

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"

difft_client = DifftClient(APPID, APPSECRET)
class TestWebsocket(unittest.TestCase):
    def test_start(self):
        listener = DifftWsListener(APPID, APPSECRET)
        # set you message handler
        listener.handler(customized_handler)
        listener.start()

def customized_handler(msg):
    # skip type RECEIPT
    if msg.get('type')=='TEXT':
        logging.info('customized handler in')
        logging.info(msg.get('msg').get('body'))
        logging.info('customized handler out')
        
        message = MessageRequestBuilder() \
                .sender("+60000")          \
                .to_user([msg.get('src')]) \
                .message(msg.get('msg').get('body')) \
                .build()
        difft_client.send_message(message)