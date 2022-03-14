# Difft-sdk-python
## Build 
```shell
make build
```

## Install
```shell
make install
```

## Example
```python
import requests
import json

from difft.auth import Authenticator

"""
发送消息
"""
my_auth = Authenticator(appid="06d4bdffbfaeef75a52e", key="KyYfHvRUpVr9NlLSVUZTOE6VPLQd".encode("utf-8"))

body = {"version": 1,"src": "+85533430156","dest": { "wuid": ["+74708405548"],"type": "USER"},"type": "TEXT","timestamp": 1646105966000,"msg": {"body": "test"}}
url = "https://openapi.test.difft.org/v1/messages"
resp = requests.post(url=url, json=body, auth=my_auth)
data = json.loads(resp.text)
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
