'''
DATE   : 12/29/2021
AUTHORS: Devin Whitten & Austin Stockwell
EMAIL  :  dev.sofiat@gmail.com
SoFIAT Capital (All rights reserved)
'''
################################################################################
# SoFIAT modules
from singularity.base import BaseAPI
from singularity import DataBaseAPI
#Python Modules
import os
import json
import pandas as pd
import requests
import hashlib
import hmac
from datetime import datetime
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

################################################################################
class BinanceAPI(BaseAPI):
    def __init__(self):
        super().__init__()

        self.keychain = {"api_key"    : os.environ.get('binance_api'),
                         "secret_api" : os.environ.get('binance_secret'),
                         "basepoint"   : "https://api.binance.us/"
                         }
        #General Endpoints
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
            'symbolOrderBookTicker'   : 'api/v3/ticker/bookTicker',
            'testNewOrder'            : 'api/v3/order/test'
        }
        # TRADING ENDPOINTS
        self._endpoints.update({
                'newOrderTrades'     : 'api/v3/order',
                'testNewOrder'       : 'api/v3/order/test',
                'queryOrder'         : 'api/v3/order',
                'cancelOrder'        : 'api/v3/order',
                'cancelAllOrders'    : 'api/v3/openOrders',
                'currentOpenOrders'  : 'api/v3/openOrders',
                'allOrders'          : 'api/v3/allOrders',
                'newOCO'             : 'api/v3/order/oco',
                'cancelOCO'          : 'api/v3/orderList',
                'queryOCO'           : 'api/v3/orderList',
                'queryAllOCO'        : 'api/v3/allOrderList',
                'queryOpenOCO'       : 'api/v3/openOrderList',
                'accountInfo'        : 'api/v3/account',
                'accountTradeList'   : 'api/v3/myTrades'
                })
        return


    def TestConnectivity(self):
        """TESTCONNECTIVITY ENDPOINT OF BINANCE API"""
        # Make GET request to Binance API & self.log out url
        url = self.keychain.get('basepoint') + self._endpoints.get('testConnectivity')
        r = requests.get(url)
        self.log(r.content)
        return r.content


    def CheckServerTime(self):
        """CHECKSERVERTIME ENDPOINT OF BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('checkServerTime')
        r = requests.get(url)
        self.log(r.content)
        return json.loads(r.content)


    def ExchangeInfo(self):
        """EXCHANGEINFO ENDPOINT of BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('exchangeInfo')
        r = requests.get(url)
        self.log(r.content)
        return r.content


    def OrderBook(self, symbol, limit):
        """ORDERBOOK ENDPOINT of BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('orderBook') + '?symbol={}&limit={}'.format(symbol, limit)
        r = requests.get(url)
        self.log(r.content)


    def SymbolPriceTicker(self, symbol= 'BTCUSDT'):
        """SYMBOLPRICETICKER ENDPOINT of BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('symbolPriceTicker') + '?symbol={}'.format(symbol)
        r = requests.get(url)
        response = json.loads(r.content)
        return response


    def CandleStick(self, symbol = 'BTCUSDT', interval='1h', **params):
        """CANDLESTICK ENDPOINT of BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('candleStick')
        body = '?symbol={}&interval={}'.format(symbol,interval)
        if params:
            body += '&' + '&'.join(f'{key}={value}' for key, value in params.items())
        url += body
        #self.log(url)
        self.response = json.loads(requests.get(url).content)
        frame = pd.DataFrame([self._format_kline(kline) for kline in self.response])
        frame['symbol'] = [symbol] * len(frame)
        return frame


    def CurrentAveragePrice(self, symbol = "BTCUSDT"):
        """CURRENTAVERAGE ENDPOINT of BINANCE API"""
        url = self.keychain.get('basepoint') + self._endpoints.get('currentAveragePrice')
        url += '?symbol={}'.format(symbol)
        self.response = json.loads(requests.get(url).content)
        self.log(self.response)
        return self.response

    ############################################################################
    # TRADING ENDPOINTS
    ############################################################################
    def NewOrder(self, **params):
        """Creates a LIVE ORDER"""
        session = requests.Session()
        url = self.keychain.get('basepoint') + self._endpoints.get('newOrderTrades')

        self.log('Testing successful, executing order..')
        if params.get("timestamp", None) is None:
            params['timestamp'] = self.current_timestamp
        # Add hash signature to params payload
        params.update(self.gen_authenticator(params))
        headers = self.gen_headers()
        body = self.gen_payload(params)
        print(params)
        session.headers.update(headers)
        # ? symbol separates the endpoint (page) from encoded information
        url += '?' + body
        self.log(url)
        self.log("Sending Order Request {}")#.format(json.dumps(params, indent=4)))
        #self.response = requests.post(url, headers).content
        self.response = json.loads(session.post(url).content)
        #self.response = test_payloads.ORDER_RESPONSE
        self.log(json.dumps(self.response, indent = 4))
        session.close()
        return self.response


    def TestNewOrder(self, **params):
        """TEST HASHED ORDER IN BINANCE API"""
        # Hit TestNewOrder endpoint
        session = requests.Session()
        url = self.keychain.get('basepoint') + self._endpoints.get('testNewOrder')

        if params.get("timestamp", None) is None:
            params['timestamp'] = self.current_timestamp

        # Add hash signature to params payload
        params.update(self.gen_authenticator(params))
        headers = self.gen_headers()
        body = self.gen_payload(params)
        session.headers.update(headers)
        #print(params)
        # ? symbol separates the endpoint (page) from encoded information
        url += '?' + body
        #self.log(url)
        self.log("Sending Order Request") #.format(json.dumps(params, indent=4)))
        self.response = json.loads(session.post(url).content)
        #self.response = json.loads(session.post(url).content)
        self.log(json.dumps(self.response, indent = 4))
        session.close()
        return self.response


    def gen_authenticator(self, params):
        """CREATE HASHED MESSAGE TO SEND TO BINANCE API"""
        self.log("Authenticating... ")
        # format params to payload
        payload = self.gen_payload(params)
        # Encoding of secret and payload
        byte_secret = self.encode(self.keychain.get("secret_api"))
        byte_payload = self.encode(payload)
        # Creates hash object with (secret, payload)
        hasher = hmac.new(byte_secret, byte_payload, digestmod='sha256')
        # Hash entire message (SecretKey, Payload)
        return {'signature' : hasher.hexdigest()}

    def AccountInfo(self, **params):
        """ACCOUNTINFORMATION ENDPOINT of BINANCE API"""
        session = requests.Session()
        url = self.keychain.get('basepoint') + self._endpoints.get('accountInfo')
        if params.get('timestamp', None) is None:
            params['timestamp'] = self.current_timestamp
        params.update(self.gen_authenticator(params))
        headers = self.gen_headers()
        body = self.gen_payload(params)
        session.headers.update(headers)
        url += '?' + body
        self.log(url)
        self.response = json.loads(session.get(url).content.decode('utf-8'))
        #self.log(self.response)
        session.close()
        return self.response

    ######################################################
    # CONCATONATES PAYLOAD (BINANCE API PARAMETERS)
    @staticmethod
    def gen_payload(params):
        return '&'.join(f'{key}={value}' for key, value in params.items())

    # ENCODES ALL PASSED TO UTF-8
    @staticmethod
    def encode(body, encoding = 'utf-8'):
        return bytes(body, encoding=encoding)

    def gen_headers(self):
        return {'Content-Type' : 'application/x-www-form-urlencoded',
                'X-MBX-APIKEY' : self.keychain.get('api_key')}

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
        kline_frame['open_time']  = '{}'.format(self.from_timestamp(kline_frame['open_time']/1000))
        kline_frame['close_time'] = '{}'.format(self.from_timestamp(kline_frame['close_time']/1000))
        return kline_frame
