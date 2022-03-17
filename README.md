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
### Send message
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
### Send attachment
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder
from difft.attachment import AttachmentBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# 1. first, upload attachment
plain_attachment = utils.random_str(1024).encode("utf-8")
uploaded_attachment = self.difft_client.upload_attachment("+60000", [], ["+76459652574"], plain_attachment) 

# 2. second, construct attachment info
attachment = AttachmentBuilder()\
                .authorize_id(uploaded_attachment.get("authorizeId"))\
                .key(uploaded_attachment.get("key"))\
                .file_size(uploaded_attachment.get("fileSize"))\
                .file_name("test.txt")\
                .digest(uploaded_attachment.get("cipherHash"))\
                .build()

# frequency limit
time.sleep(1)

# 3. third, send message with attachment
message = MessageRequestBuilder()                           \
            .sender("+60000")                               \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7")   \
            .message("hello, this is a test message")       \
            .at_user(["+76459652574"])                      \
            .attachment(attachment)                         \
            .timestamp_now()\
            .build()
self.difft_client.send_message(message)
```

## Run test
```shell
python3 -m unittest discover
```

# TODO
* [x] Auth
* [x] Attachment APIs
* [x] Message APIs
* [ ] Group APIs
* [ ] Account APIs
* [ ] Team APIs

# CHANGELOG
## 2022.3.16
1. support send message
2. support uploand and download attachment
3. support append and remove attachment authorization

## init
1. support authentication
