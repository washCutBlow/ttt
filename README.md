# Difft-sdk-python
## Install from python package
```shell
pip install https://git.toolsfdg.net/difftim/difft-sdk-python/releases/download/v1.0.0/difft-1.0.0-py3-none-any.whl
```

## Install from source code
```shell
make install
```

## Example
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# send message to individuel user
message = MessageRequestBuilder()                     \
            .sender(BOT_ID)                           \
            .to_user(["+76459652574"])                \
            .message("hello, this is a test message") \
            .build()

difft_client.send_message(message)

# sleep 1 second due to server-end frequency limit
time.sleep(1)

# send message to group
message = MessageRequestBuilder()                         \
            .sender(BOT_ID)                               \
            .to_group("a9de6b3ae8c8456d888c4532b487e822") \
            .message("hello, this is a test message")     \
            .at_user(["+76459652574"])                    \
            .build()
difft_client.send_message(message)
```

## Run test
```shell
python3 -m unittest discover
```

# TODO
* [x] Auth
* [ ] Attachment APIs
* [ ] Group APIs
* [ ] Account APIs
* [ ] Team APIs
