#CHOOSE TIME INTERVAL AND GET THAT TO WORK
# decision -- BUY OR SELL AS OUTPUT TO CONSOLE
import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
import time
import json
import pandas as pd
import numpy as np
import schedule
import logging
import requests


logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO)
log = logging.Logger('test')


# USED FOR COMMON METHODS IN BINANCE API HELPER CLASSES
class BaseAPI(object):
    def __init__(self):
        self.keychain = {"api_key"    : os.environ.get('binance_api'),
                         "secret_api" : os.environ.get('binance_secret'),
                         "mysql_key"  : os.environ.get('mysql_key'),
                         "endpoint"   : "https://api.binance.com/",
                    }

        self.cnx = mysql.connector.connect(user='root',
                                      password=self.keychain.get('mysql_key', None),
                                      host='127.0.0.1',
                                      database='stockportfolio',
                                      auth_plugin='mysql_native_password')

    @property
    def _get_current_time(self):
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp


    # OBTAINS VALUE STORED IN DATABASE ASSOCIATED WITH TICKER PASSED
    def _get_ticker_id(self, ticker):
        # SELECT gets the associated product NUMBER from the ticker passed
        select_stmt = "SELECT idproduct FROM product WHERE ticker = '{}'".format(ticker)

        cursor = self.cnx.cursor()
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        result = np.array(result).flatten()[0]   # List becomes single value
        cursor.close()
        return result


    def log(self, msg=""):
        print('{} - Binance API : {}'.format(self._get_current_time, msg))
        return


# CLASS PERFORMS ALL MANIPULATION OF MYSQL TABLES
class BinanceAPI(BaseAPI):
    def __init__(self):
        self.log('initializing BinanceAPI')
        BaseAPI.__init__(self)
        return

    ############################################################################
    # TIMING RELATED
    # TIMER THAT CHANGES SAMPLING RATE OF SPECIFIED FUNCTIONS
    def run(self, interval=10):
        schedule.every(interval).seconds.do(self.query)
        #schedule.every(interval).seconds.do(self.monitor)
        while True:
            self.log('running... ')
            schedule.run_pending()
            time.sleep(interval)
        return

    # FORMATS BINANCE API TIMESTAMP INTO READABLE (D:H:M:S) FORMAT
    def time(self):
        url = "api/v3/time"
        endpoint = self.keychain.get('endpoint') + url
        try:
            self.response = json.loads(requests.get(endpoint).text)
            time = self.response.get('serverTime')
            self.log(time)
            self.log(datetime.fromtimestamp(int(time)/1000))
        except:
            self.response = {}
        return self.response

    @staticmethod
    def from_timestamp(timestamp):
        return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')

    ############################################################################
    # BINANCE WEB API FUNCTIONS
    # CALLS KLINE ENDPOINT IN BINANCE API
    def kline(self, **params):  #myFunction(self,dictionary)
        '''Precondition: acceptes symbol (needed), limit, interval='1hr/1d/etc'
        '''
        assert 'symbol' in params.keys(), 'need symbol in kline()'

        url = 'api/v3/klines?' + '&'.join(f'{key}={value}' for key, value in params.items())
        endpoint = self.keychain.get('endpoint') + url
        self.log(endpoint)
        self.response = json.loads(requests.get(endpoint).text)
        frame = pd.DataFrame([self._format_kline(kline) for kline in self.response])
        frame['symbol'] = [params.get('symbol')] * len(frame)

        return frame


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

    # MAKES GET REQUEST TO BINANCE API TO RETRIEVE CURRENT PRICES
    def get_price(self, currency = "BTCUSDT"):
        url = 'api/v3/avgPrice?symbol='
        try:
            endpoint = self.keychain.get("endpoint") + url + currency
            self.log(endpoint)
            self.response = json.loads(requests.get(endpoint).text)
            self.log(self.response)
        except:
            self.response = {}
        return self.response

    ############################################################################
    # SQL RELATED FUNCTIONS
    # INSERTS REAL TIME PRICE DATA THAT IS OBTAINED FROM API

    def insertDayCandle(self, daycandles):
        '''Precondition: daycandles is the result of self.kline
        '''
        columns = ['close_time', 'low', 'high', 'open', 'close', 'volume']

        for column in columns[1:]:
            daycandles[column] = np.array(daycandles[column], dtype=float)

        mySql_insert_query = """INSERT INTO dayCandle (iddayCandle, fk_idproduct_dayCandle, date, low, hi, open, close, volume)
                               VALUES
                               (null, %s, %s, %s, %s, %s, %s, %s) """

        cursor = self.cnx.cursor()

        for i, candle in daycandles.iterrows():
            symbol_id = self._get_ticker_id(candle['symbol'])
            recordTuple = list(candle[columns])
            recordTuple.insert(0, str(symbol_id))
            cursor.execute(mySql_insert_query, recordTuple)
            self.cnx.commit()


        self.log('Record inserted successfully into dayCande {}'.format(cursor.rowcount))
        cursor.close()
        return


    def query(self, currency = "BTCUSDT"):
        timestamp = self._get_current_time
        response = self.get_price(currency)

        price = float(response.get("price"))

        mySql_insert_query = """INSERT INTO realtime (idrealtime, fk_idproduct_realTime, observedPrice, observedTime)
                               VALUES
                               (null, 1, %s, %s) """

        recordTuple = (price, timestamp)
        cursor = self.cnx.cursor()
        cursor.execute(mySql_insert_query, recordTuple)
        self.cnx.commit()
        self.log('Record inserted successfully into table {}'.format(cursor.rowcount))
        cursor.close()
        return

    # ENTERS DATA INTO TRANSACTION TO TRACK TRADE HISTORY
    def transaction(self, input_ticker, value=0):
        product_id = self._get_ticker_id(input_ticker)

        mySql_insert_query = """INSERT INTO transaction (idtransaction, fk_idproduct_transaction, transactionTime, buySell, price) VALUES (null, %s, %s, true, %s)"""
        timestamp = self._get_current_tim

        #self.log('Timestamp:  ', timestamp)
        recordTuple = (str(product_id), timestamp, str(value))
        self.log('recordTuple', recordTuple)
        cursor = self.cnx.cursor()
        self.log('Executing....')
        cursor.execute(mySql_insert_query, recordTuple)
        self.cnx.commit()
        cursor.close()
        self.log('Success')
        return

    #def __del__(self):
    #    self.log("closing API...")
    #    self.cnx.close()



############################################################################
#MAIN CODE MAIN CODE MAIN CODE MAIN
############################################################################
if __name__ == '__main__':
    api = BinanceAPI()  #Creates object (instance of BinanceAPI class)
    #api.run()
    api.time()

    '''  FOR TESTING
    result = api.kline(symbol='BTCUSDT', limit=2, interval='1d'

    for ticker in symbols:

        print("...get_price:  ", ticker)
        api.get_price(ticker)

        print("...query", ticker)
        api.query(currency = ticker)
        api.query(currency = ticker)
    '''
