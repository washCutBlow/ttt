import requests
import collections
import hmac, hashlib
from urllib.parse import urlparse, parse_qs

from difft.utils import *
from difft.constants import *

class Signature:
    def __init__(self, timestamp: int, nonce: str, algorithm: str, signature: str) -> None:
        self.timestamp = timestamp
        self.nonce = nonce
        self.algorithm = algorithm
        self.signature = signature

class Authenticator(requests.auth.AuthBase):
    def __init__(self, appid: str, key: bytes, headers: list=None) -> None:
        self._appid = appid
        self._key = key
        if headers:
            headers.append("Content-Type")
            headers.append("Content-Length")
        else:
            headers = ["Content-Type", "Content-Length"]
        self._headerToSign = headers

    def __call__(self, r):
        method = r.method

        parsed_url = urlparse(r.url)

        uri = parsed_url.path
        query_parameters = parse_qs(parsed_url.query)
        sorted_query_parameters = collections.OrderedDict(sorted(query_parameters.items()))

        headers = r.headers
        headerToSign = {}
        headerToSignList = []
        for k in headers:
            if k in self._headerToSign:
                headerToSign[k] = headers[k]
                headerToSignList.append(k)
        
        headerToSignStr = ",".join(headerToSignList)
        
        sorted_headers = collections.OrderedDict(sorted(headerToSign.items()))

        body = r.body
        
        dataToSign = self.build_data(method, uri, sorted_query_parameters, sorted_headers, body)
        signature = self.sign(dataToSign)
        new_headers = {
            HEADER_NAME_APPID: self._appid,
            HEADER_NAME_TIMESTAMP: signature.timestamp,
            HEADER_NAME_NONCE: signature.nonce,
            HEADER_NAME_ALGORITHM: signature.algorithm,
            HEADER_NAME_SIGNEDHEADERS: headerToSignStr,
            HEADER_NAME_SIGNATURE: signature.signature,
        }
        r.headers.update(new_headers)
        return r
    
    def build_data(self, method: str, uri: str, parameters: dict, headers: dict, body: bytes) -> bytes:
        data = method + ";" + uri + ";"
        for k in parameters:
            for i in parameters[k]:
                data += k + "=" + i + ","
        data = data[:-1]
        data += ";"

        for k in headers:
            data += k.lower() + "=" + headers[k] + ","
        
        data = data[:-1]
        data += ";"
        data = data.encode("utf-8")
        if body:
            data += body
        
        return data
    
    def sign(self, msg: bytes) -> Signature:
        ts = current_milli_time()
        nonce = get_nonce()
        data = ";".join([self._appid, str(ts), nonce]) + ";" 
        msg = data.encode("utf-8") + msg
        sign_str = hmac.new(self._key, msg, hashlib.sha256).hexdigest()
        signature = Signature(timestamp=ts, nonce=nonce, algorithm=ALGORITHM_HMAC_SHA256, signature=sign_str)
        return signature
