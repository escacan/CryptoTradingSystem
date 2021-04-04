import os
import uuid
import time

import jwt
import requests

import pandas as pd
import pprint
import pyupbit

import datetime

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']
upbit = pyupbit.Upbit(access_key, secret_key)

_LAST_CHECKED_DATE = 0
_LAST_CHECKED_MIN = 0
_NOTIONAL_BALANCE = 3000000
_MAXIMUM_RISK = 0.01

def getCoinList():
    return pyupbit.get_tickers(fiat="KRW")

def getCurrentPrice(ticket):
    pprint.pprint(pyupbit.get_current_price(ticket))

def getAccountInfo():
    print(upbit.get_balance("KRW"))

def calculateUnitSize(coin, atr):
    unitSize = 0
    print("Can order {} : {}".format(coin, unitSize))

    maximumSL = _NOTIONAL_BALANCE * _MAXIMUM_RISK
    # get Dollar per point
    # calculate Maximum SL price
    # get Minimum Order Size

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

def clearOrders():
    coinList = getCoinList()
    for coin in coinList:
        # Remove pending orders
        orderId = upbit.get_order(coin)['uuid']
        upbit.cancel_order(orderId)

        # Clear every coin positions
        leftCoin = upbit.get_balance(coin))
        upbit.sell_market_order(coin, leftCoin))

if __name__ == "__main__":
    getAccountInfo()
    today = datetime.date.today()

    if _LAST_CHECKED_DATE != today:
        _LAST_CHECKED_DATE = today
        # Cancle Orders
        upbit.get_order("KRW-LTC")

        updateMarketInfo()

    currentMin = datetime.time.minute()
    if _LAST_CHECKED_MIN != currentMin:
        # Check Price
        _LAST_CHECKED_MIN = currentMin
        coinList = getCoinList()
        print(pyupbit.get_current_price(coinList))


    # 현재 계좌의 상황 체크하기
    # getAccountInfo()
    # getMinCandle(15, "KRW-BTC",300)
    # getDayCandle("KRW-BTC", 55)
