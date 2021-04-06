import csv
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
_NOTIONAL_BALANCE = 3000000
_MAXIMUM_RISK = 0.01

_ATR_BASE_TERM = 4

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
    targetCoinDic = {}

    for coin in coinList:
        time.sleep(0.1)
        df = pd.DataFrame(pyupbit.get_ohlcv(ticker=coin, interval="day", count=_ATR_BASE_TERM))
        atrSeries = pd.Series(data=df['high'] - df['low'], index=df.index)

        if len(df) < _ATR_BASE_TERM:
            continue

        yesterdayInfo = df.iloc[-1]
        beforeYesterdayInfo = df.iloc[-2]

        if atrSeries[-1] == atrSeries.min():
            if beforeYesterdayInfo['high'] >= yesterdayInfo['high'] and beforeYesterdayInfo['low'] <= yesterdayInfo['low']:
                targetCoinDic[coin] = {'목표가': yesterdayInfo['high'], '손절가': yesterdayInfo['low'], '보유여부': False}

    marketInfoDf = pd.DataFrame(data=targetCoinDic).T
    pprint.pprint(marketInfoDf)
    return marketInfoDf

def clearOrders():
    coinList = getCoinList()
    for coin in coinList:
        # Remove pending orders
        orderId = upbit.get_order(coin)['uuid']
        upbit.cancel_order(orderId)

        # Clear every coin positions
        leftCoin = upbit.get_balance(coin)
        upbit.sell_market_order(coin, leftCoin)


if __name__ == "__main__":
    print("Start NR{} Trading".format(_ATR_BASE_TERM))

    f = open('OrderLog.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['날짜', '코인이름', '목표가', '손절가', '실제 결과'])
    f.close()
    todayMarketInfoDf = 0

    while True:
        today = datetime.date.today()
        if _LAST_CHECKED_DATE != today:
            _TARGET_COIN_INFO = {}
            _LAST_CHECKED_DATE = today

            todayMarketInfoDf = updateMarketInfo()

        # Check Price
        coinList = todayMarketInfoDf.index
        # print(pyupbit.get_current_price(coinList))
        currentPrice = pd.Series(data=pyupbit.get_current_price(coinList))

        pprint.pprint(currentPrice)
        break
        #
        # for coin in coinList:
        #     if coin in currentPrice.
        #     if _MARKET_INFO.loc[coin]["조건달성"] is True and currentPrice[coin] >= _MARKET_INFO.loc[coin]['목표가']:
        #         currentTime = datetime.datetime.strftime('%c')
        #         print("{}:: Send order for {}".format(currentTime, coin))
        #         time.sleep(0.1)

        time.sleep(1)

    # 현재 계좌의 상황 체크하기
    # getAccountInfo()
    # getMinCandle(15, "KRW-BTC",300)
    # getDayCandle("KRW-BTC", 55)
