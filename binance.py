import ccxt
import pprint
import pandas as pd

def getMarketInfo():
    binance = ccxt.binance()
    markets = binance.load_markets()

    print(markets.keys())
    print(len(markets))

def getCurrentPrice():
    binance = ccxt.binance()
    btc = binance.fetch_ticker("BTC/USDT")
    pprint.pprint(btc)

def get15MinCandles():
    binance = ccxt.binance()
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '15m')

    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    print(df)

def get1DayCandles():
    binance = ccxt.binance()
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d')

    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    print(df)


if __name__ == "__main__":
    # getMarketInfo()
    # getCurrentPrice()
    get15MinCandles()
    get1DayCandles()