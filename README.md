# Difft-sdk-python
## Interface
* send_message
* get_account_by_email
* get_account_by_wuid
* get_group_by_botid
* upload_attachment
* download_attachment

## Command-line
DiffClient provide a command-line tool `difft-cli`, before using `difft-cli`, you should create a configure file `.difft.cfg` in current directory or HOME directory, e.g
```cfg
[base]
appid=f250845b274f4a5c01
secret=w0m6nTOIIspxR0wmGJbEvAOfNnyf
botid=+60000
host=https://openapi.test.difft.org
``` 
Also, you can provide the above configuration in command line, e.g
```shell
difft-cli --appid f250845b274f4a5c01 --secret w0m6nTOIIspxR0wmGJbEvAOfNnyf --botid +60000 --host https://openapi.test.difft.org sendmsg -user +76459652574 -msg "hello world"
```
### Example
After creating configure file `.difft.cfg` in current directory or HOME directory, you can simply use `difft-cli` as below:
```shell
# send message to user
difft-cli sendmsg -user +76459652574 -msg "hello world"

# send message to group
difft-cli sendmsg -group a9de6b3ae8c8456d888c4532b487e822 -msg "hello world"

# send attachment
difft-cli sendmsg -user +76459652574 -att test.txt

# send image 
difft-cli sendmsg -user +76459652574 -att test.jpg -att-type image/jpeg

# get account
difft-cli account -email xxx1@xxx,xxx2@xxxx

# get group by botid
difft-cli group -bot +60000

```

## Install from python package
```shell
pip install difft
```

## Install from source code
```shell
make install
```

## Using as a python module
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

# send message to users
message = MessageRequestBuilder()                     \
            .sender(BOT_ID)                           \
            .to_user(["+76459652574"])                \
            .message("hello, this is a test message") \
            .timestamp_now()                          \
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
            .timestamp_now()                              \
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

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# 1. first, upload attachment
plain_attachment = utils.random_str(1024).encode("utf-8")
uploaded_attachment = difft_client.upload_attachment("+60000", [], ["+76459652574"], plain_attachment) 

# 2. second, construct attachment info
attachment = AttachmentBuilder()\
                .authorize_id(uploaded_attachment.get("authorizeId"))   \
                .key(uploaded_attachment.get("key"))                    \
                .file_size(uploaded_attachment.get("fileSize"))         \
                .file_name("test.txt")                                  \
                .digest(uploaded_attachment.get("cipherHash"))          \
                .build()

# 3. third, send message with attachment
message = MessageRequestBuilder()                           \
            .sender("+60000")                               \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7")   \
            .message("hello, this is a test message")       \
            .at_user(["+76459652574"])                      \
            .attachment(attachment)                         \
            .timestamp_now()                                \
            .build()
difft_client.send_message(message)
```

### Send image
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder
from difft.attachment import AttachmentBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# 1. first, upload img
with open("{/path/to/img}", "rb") as f:
    img = f.read()
uploaded_img = difft_client.upload_attachment("+60000", [], ["+76459652574"], img) 

# 2. second, construct attachment info
# content_type: depend on img extention
attachment = AttachmentBuilder()\
                .authorize_id(uploaded_img.get("authorizeId"))   \
                .key(uploaded_img.get("key"))                    \
                .file_size(uploaded_img.get("fileSize"))         \
                .file_name("test.jpg")                           \
                .content_type("image/jpeg")                      \
                .digest(uploaded_img.get("cipherHash"))          \
                .build()

# 3. third, send message with attachment
message = MessageRequestBuilder()                           \
            .sender("+60000")                               \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7")   \
            .at_user(["+76459652574"])                      \
            .attachment(attachment)                         \
            .timestamp_now()                                \
            .build()
difft_client.send_message(message)
```
### Get Account info
```python
difft_client.get_account_by_email("xxx@xxx")
# get multiple account info by email
difft_client.get_account_by_email("xxx@xxx,xxx@xxx")


difft_client.get_account_by_wuid("xxx")
# get multiple account info by wuid
difft_client.get_account_by_wuid("xxxx,xxx")
```
### Get Group info
```python
difft_client.get_group_by_botid("xxx")
```

## Run test
```shell
python3 -m unittest discover
```

# TODO
* [x] Auth
* [x] Attachment APIs
* [x] Message APIs
* [x] Account APIs
* [x] Group APIs
* [ ] Team APIs

# CHANGELOG
## 2022.3.26
1. support command-line tool 

## 2022.3.24
1. support get group

## 2022.3.23
1. support get account

## 2022.3.18
1. send message return failed list
2. support set content-type when send attachment

## 2022.3.16
1. support send message
2. support uploand and download attachment
3. support append and remove attachment authorization

## init
1. support authentication
