import requests, json
from difft.auth import Authenticator

APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID = "+60000"

'''
First, invite the bot into the your group.
Then run this script to get group info
'''

# testing env
URL = "https://openapi.test.difft.org/v1/groups"
# production env
# URL = "https://openapi.difft.org/v1/groups"

my_auth = Authenticator(appid=APPID, key=APPSECRET.encode("utf-8"))

"""query group info of bot"""
resp = requests.get(url=URL, params={"operator":BOT_ID}, auth=my_auth)
data = json.loads(resp.text)
print(data)