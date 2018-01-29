import hashlib
import hmac
import base64

import requests
import json

import pandas as pd

def signa(msg, secret):
    message = bytes(msg).encode('utf-8')
    secret = bytes(secret).encode('utf-8')

    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    return(signature)

def kline():
    url = "https://api.huobi.pro/market/history/kline"
    response = requests.get(url)
    json_res = response.json()
    return (json.dumps(json_res["status"]),\
        json.dumps(json_res["ch"]),\
        pd.read_json(json.dumps(json_res["data"])))
