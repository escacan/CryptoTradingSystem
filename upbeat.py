import os
import uuid
import time

import jwt
import requests

import pandas as pd
import pprint
import pyupbit

from datetime import date

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']
upbit = pyupbit.Upbit(access_key, secret_key)

lastDate = 0

def getCoinList():
    return pyupbit.get_tickers(fiat="KRW")

def getCurrentPrice(ticket):
    pprint.pprint(pyupbit.get_current_price(ticket))

def getAccountInfo():
    print(upbit.get_balance("KRW"))

def updateMarketInfo():
    coinList = getCoinList()
    for coin in coinList:
        time.sleep(0.1)
        df = pd.DataFrame(pyupbit.get_ohlcv(ticker= coin, interval= "day", count= 4))
        atrSeries = pd.Series(data= df['high'] - df['low'], index=df.index)

        yesterdayInfo = df.iloc[-1]
        beforeYesterdayInfo = df.iloc[-2]

        if atrSeries[-1] == atrSeries.min():
            if beforeYesterdayInfo['high'] >= yesterdayInfo['high'] and beforeYesterdayInfo['low'] <= yesterdayInfo['low']:
                print("Send buylimit order for {} on {} and SL on {}".format(coin, yesterdayInfo['high'], yesterdayInfo['low']))

if __name__ == "__main__":
    getAccountInfo()
    today = date.today()

    if lastDate != today:
        lastDate = today
        updateMarketInfo()


    # 현재 계좌의 상황 체크하기
    # getAccountInfo()
    # getMinCandle(15, "KRW-BTC",300)
    # getDayCandle("KRW-BTC", 55)
