import ccxt

def getMarketInfo():
    binance = ccxt.binance()
    markets = binance.load_markets()

    print(markets.keys())
    print(len(markets))

if __name__ == "__main__":
    getMarketInfo()
