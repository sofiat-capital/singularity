# MARKET DATA ENDPOINTS
from .base_api import BaseAPI
import os
import json
import requests
import pandas as pd
################################################################################
# ENDPOINTS LIST: CAMEL CASE NOTATION
################################################################################
ENDPOINTS = {
'testConnectivity'        : '/api/v3/ping',
'checkServerTime'         : '/api/v3/time',
'exchangeInfo'            : '/api/v3/exchangeInfo',
'orderBook'               : '/api/v3/depth',
'recentTradesList'        : '/api/v3/trades',
'oldTradeLookup'          : 'api/v3/historicalTrades',
'aggregateTradesList'     : '/api/v3/aggTrades',
'candleStick'             : '/api/v3/klines',
'currentAveragePrice'     : '/api/v3/avgPrice',
'dailyTickerPriceChange'  : '/api/v3/ticker/24hr',
'symbolPriceTicker'       : '/api/v3/ticker/price',
'symbolOrderBookTicker'   : '/api/v3/ticker/bookTicker'
}

# ACCOUNT ENDPOINTS
newOrderTrades = '/api/v3/order  (HMAC SHA256)' #POST
testNewOrder = '/api/v3/order/test (HMAC SHA256)' #POST
queryOrder = 'api/v3/order (HMAC SHA256)' #GET
cancelOrder = 'api/v3/order (HMAC SHA256)' #DELETE
cancelAllOrders = '/api/v3/openOrders (HMAC SHA256)' #DELETE
currentOpenOrders = '/api/v3/openOrders  (HMAC SHA256)' #GET
allOrders = '/api/v3/allOrders (HMAC SHA256)' #GET
newOCO = '/api/v3/order/oco (HMAC SHA256)' #POST
cancelOCO = '/api/v3/orderList (HMAC SHA256)' #DELETE
queryOCO = '/api/v3/orderList (HMAC SHA256)' #GET
queryAllOCO = '/api/v3/allOrderList (HMAC SHA256)' #GET
queryOpenOCO = '/api/v3/openOrderList (HMAC SHA256)' #GET
accountInfo = '/api/v3/account (HMAC SHA256)' #GET
accountTradeList = '/api/v3/myTrades  (HMAC SHA256)' #GET

# USER STREAM ENDPOINTS
startUserDataStream = '/api/v3/userDataStream' #POST
keepAliveUserDataStream = '/api/v3/userDataStream' #PUT
closeUserDataStream = '/api/v3/userDataStream'#DELETE



################################################################################
# ENDPOINTS FUNCTIONS
################################################################################
class BinanceAPI(BaseAPI):
    def __init__(self):
        BaseAPI.__init__(self)
        self.keychain = {"api_key"    : os.environ.get('binance_api'),
                         "secret_api" : os.environ.get('binance_secret'),
                         "basepoint"   : "https://api.binance.com/"
                         }

        self._endpoints = {
        'testConnectivity'        : 'api/v3/ping',
        'checkServerTime'         : 'api/v3/time',
        'exchangeInfo'            : 'api/v3/exchangeInfo',
        'orderBook'               : 'api/v3/depth',
        'recentTradesList'        : 'api/v3/trades',
        'oldTradeLookup'          : 'pi/v3/historicalTrades',
        'aggregateTradesList'     : 'api/v3/aggTrades',
        'candleStick'             : 'api/v3/klines',
        'currentAveragePrice'     : 'api/v3/avgPrice',
        'dailyTickerPriceChange'  : 'api/v3/ticker/24hr',
        'symbolPriceTicker'       : 'api/v3/ticker/price',
        'symbolOrderBookTicker'   : 'api/v3/ticker/bookTicker'
        }
        return

    # TESTCONNECTIVITY ENDPOINT OF BINANCE API
    def TestConnectivity(self):
        # Make GET request to Binance API & self.log out url
        url = self.keychain.get('basepoint') + self._endpoints.get('testConnectivity')
        r = requests.get(url)
        self.log(r.content)
        return r.content

    # CHECKSERVERTIME ENDPOINT OF BINANCE API
    def CheckServerTime(self):
        url = self.keychain.get('basepoint') + self._endpoints.get('checkServerTime')
        r = requests.get(url)
        self.log(r.content)
        return r.content

    # EXCHANGEINFO ENDPOINT of BINANCE API
    def ExchangeInfo(self):
        url = self.keychain.get('basepoint') + self._endpoints.get('exchangeInfo')
        r = requests.get(url)
        self.log(r.content)

    # ORDERBOOK ENDPOINT of BINANCE API
    def OrderBook(self, symbol, limit):
        url = self.keychain.get('basepoint') + self._endpoints.get('orderBook') + '?symbol={}&limit={}'.format(symbol, limit)
        r = requests.get(url)
        self.log(r.content)

    # CANDLESTICK ENDPOINT of BINANCE API
    def CandleStick(self, symbol = 'BTCUSDT', interval='1h', **params):
        '''Precondition: acceptes symbol (needed), limit, interval='1hr/1d/etc'
        '''

        url = self.keychain.get('basepoint') + self._endpoints.get('candleStick')
        url += '?symbol={}&interval={}'.format(symbol,interval)

        if params:
            url += '&'.join(f'{key}={value}' for key, value in params.items())

        self.log(url)
        self.response = json.loads(requests.get(url).content)
        frame = pd.DataFrame([self._format_kline(kline) for kline in self.response])
        frame['symbol'] = [symbol] * len(frame)
        return frame

    # CURRENTAVERAGE ENDPOINT of BINANCE API
    def CurrentAveragePrice(self, symbol = "BTCUSDT"):
        url = self.keychain.get('basepoint') + self._endpoints.get('currentAveragePrice')
        url += '?symbol={}'.format(symbol)
        self.response = json.loads(requests.get(endpoint).content)

        self.log(self.response)
        return self.response


################################################################################
# USER DEFINED
################################################################################
    # FORMATS BINANCE API TIMESTAMP INTO READABLE (D:H:M:S) FORMAT
    def time(self):
        self.response = json.loads(requests.get(endpoint).content)
        time = self.CheckServerTime()
        time = datetime.fromtimestamp(int(time)/1000)
        return self.response

    # (HIDDEN FUNCTION) LIST COMPREHENSION CONCATONATES DESCRIPTIONS TO VALUES
    def _format_kline(self, kline):
        kline_frame = {}
        kline_map = ["open_time", "open", "high", "low", "close", "volume", "close_time", \
                    "quote_asset_volume", "number_of_trades", \
                    "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume",
                    "ignore"]

        [kline_frame.update({name : value}) for name, value in zip(kline_map, kline)]

        kline_frame['open_time']  = '{}'.format(self.from_timestamp(kline_frame['open_time']))
        kline_frame['close_time'] = '{}'.format(self.from_timestamp(kline_frame['close_time']))
        return kline_frame
