import os
import ccxt
import pprint
import pandas as pd

_N_VALUE = 0
_BREAKOUT_TERM = 55
_PROFIT_TERM = 20
_RISK = 0.01
_TOTAL_UNIT_COUNT = 0



def get_account_balance():
    # binance 객체 생성
    binance = ccxt.binance(config={
        'apiKey': os.environ['BINANCE_APP_KEY'],
        'secret': os.environ['BINANCE_SECRET_KEY']
    })

    # USDT의 잔고 조회
    balance = binance.fetch_balance()
    # print(balance)
    print(balance['free'])
    # print(balance['USDT'])

def get_market_info():
    binance = ccxt.binance()
    markets = binance.load_markets()

    print(markets.keys())
    print(len(markets))

def get_current_price():
    binance = ccxt.binance()
    btc = binance.fetch_ticker("BTC/USDT")
    pprint.pprint(btc)

def get_15min_candles():
    binance = ccxt.binance()
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '15m')

    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    print(df)

def get_1day_candles():
    binance = ccxt.binance()
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d')

    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    # print(df)
    return df

def calculate_atr_values():
    df = get_1day_candles()
    atr_values = pd.DataFrame({
        'atr': df['high'] - df['low']
    })
    # print(atr_values)

    atr_values = atr_values.tail(21)[:-1]
    print(atr_values)
    _N_VALUE = atr_values.mean()

def calculate_breakout_price():
    df = get_1day_candles()
    price_55days = df.tail(51)[:-1]

    buy_breakout_price = max(df['high'])
    sell_breakout_price = min(df['low'])
    print(buy_breakout_price, sell_breakout_price)

if __name__ == "__main__":
    get_account_balance()
    # getMarketInfo()
    # getCurrentPrice()
    # get_15min_candles()
    # get_1day_candles()
    calculate_atr_values()
    calculate_breakout_price()