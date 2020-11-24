import os
import numpy as np
from .base_api import BaseAPI

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

class DataBaseAPI(BaseAPI):
    def __init__(self):
        BaseAPI.__init__(self)
        self.keychain = {'mysql_key' : os.environ.get('mysql_key')}


        self.cnx = mysql.connector.connect(user='root',
                                      password=self.keychain.get('mysql_key', None),
                                      host='127.0.0.1',
                                      database='stockportfolio',
                                      auth_plugin='mysql_native_password')
        return

    ############################################################################
    ### Insert FUNCTIONS
    ############################################################################
    def InsertDayCandle(self, daycandles):
        '''Precondition: daycandles is the result of self.kline
        '''
        columns = ['close_time', 'low', 'high', 'open', 'close', 'volume', 'number_of_trades']

        for column in columns[1:-1]:
            daycandles[column] = np.array(daycandles[column], dtype=float)

        daycandles[columns[-1]] = np.array(daycandles[column], dtype=int)

        mySql_insert_query = """INSERT INTO dayCandle (iddayCandle, fk_idproduct_dayCandle, date, low, hi, open, close, volume, numtrades)
                               VALUES
                               (null, %s, %s, %s, %s, %s, %s, %s, %s) """

        cursor = self.cnx.cursor()

        for i, candle in daycandles.iterrows():
            symbol_id = self._get_ticker_id(candle['symbol'])
            recordTuple = list(candle[columns])
            recordTuple.insert(0, str(symbol_id))
            cursor.execute(mySql_insert_query, recordTuple)
            self.cnx.commit()

        self.log('Record inserted successfully into dayCandle {}'.format(cursor.rowcount))
        cursor.close()
        return

    # ENTERS DATA INTO TRANSACTION TO TRACK TRADE HISTORY
    def InsertTransaction(self, input_ticker, value=0):
        product_id = self._get_ticker_id(input_ticker)

        mySql_insert_query = """INSERT INTO transaction (idtransaction, fk_idproduct_transaction, transactionTime, buySell, price) VALUES (null, %s, %s, true, %s)"""
        timestamp = self.current_time

        recordTuple = (str(product_id), timestamp, str(value))
        self.log(recordTuple)
        cursor = self.cnx.cursor()
        self.log('Executing....')
        cursor.execute(mySql_insert_query, recordTuple)
        self.cnx.commit()
        cursor.close()
        self.log('Success')
        return


    ############################################################################
    ### HIDDEN FUNCTIONS
    ############################################################################
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
