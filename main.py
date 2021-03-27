import os
import uuid

import jwt
import requests

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

baseTimeSetting = {
    "1min": "/minutes/1",
    "5min": "/minutes/5",
    "15min": "/minutes/15",
    "day": "/days",
    "week": "/weeks",
    "month": "/months"
}

def getMinCandle(target_min, market, candle_count):
    querystring = {
        "market": market,
        "count": candle_count
    }
    res = requests.request("GET", server_url + "/v1/candles/minutes/" + str(target_min), params=querystring)

    print(res.text)


def getDayCandle(market, candle_count):
    querystring = {
        "market": market,
        "count": candle_count
    }
    res = requests.request("GET", server_url + "/v1/candles/days", params=querystring)

    print(res.text)


def getAccountInfo():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)

    print(res.json())


if __name__ == "__main__":
    # 현재 계좌의 상황 체크하기
    getAccountInfo()
    getMinCandle(15, "KRW-BTC",300)
    getDayCandle("KRW-BTC", 55)
