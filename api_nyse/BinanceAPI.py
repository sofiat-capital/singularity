#CHOOSE TIME INTERVAL AND GET THAT TO WORK
# decision -- BUY OR SELL AS OUTPUT TO CONSOLE
import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import datetime, time
import json
import numpy as np
import schedule


import requests

# CLASS PERFORMS ALL MANIPULATION OF MYSQL TABLES
class BinanceAPI(object):
    def __init__(self):

        self.params = {"api_key"    : os.environ.get('binance_api'),
                       "secret_api" : os.environ.get('binance_secret'),
                       "endpoint"   : "https://api.binance.com/",
                       "yahoo"      : 'https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch'
                    }
        return

    def get_price(self, currency = "BTCUSDT"):
        url = 'api/v3/avgPrice?symbol='
        try:
            endpoint = self.params.get("endpoint") + url + currency
            print(endpoint)
            self.response = json.loads(requests.get(endpoint).text)
            print(self.response)
        except:
            print("shit fuuuuck dude")
            self.response = {}

        return self.response

    # METHOD GETS CURRENT TIME
    @property
    def _get_current_time(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    # METHOD SCRAPES YAHOO.COM AND INSERTS DATA INTO realTime TABLE
    def query(self, currency = "BTCUSDT"):


        cnx = mysql.connector.connect(user='root', password='Th3T3chBoy$',
                                      host='127.0.0.1',
                                      database='stockportfolio')
        timestamp = self._get_current_time
        response = self.get_price(currency)

        mySql_insert_query = """INSERT INTO realtime (idrealtime, fk_idproduct_realTime, observedPrice, observedTime)
                               VALUES
                               (null, 1, %s, %s) """


        recordTuple = (response.get("price"),timestamp)
        cursor = cnx.cursor()
        cursor.execute(mySql_insert_query, recordTuple)
        cnx.commit()
        print(cursor.rowcount, "Record inserted successfully into table")
        cursor.close()
        cnx.close()

        return

    def _get_ticker_id(self, ticker):

        cnx = mysql.connector.connect(user='root', password='Th3T3chBoy$',
                                      host='127.0.0.1',
                                      database='stockportfolio')

        # SELECT gets the associated product NUMBER from the ticker passed
        select_stmt = "SELECT idproduct FROM product WHERE ticker = '{}'".format(ticker)
        cursor = cnx.cursor()
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        result = np.array(result).flatten()[0]   # List becomes single value
        cursor.close()
        print(select_stmt)
        print('RESULT:  ', result)
        return result


    def transaction(self, input_ticker, value=0):
        '''
        # Transaction Method gets passed a ticker value, finds associated Ticker# within database
        # and then inserts the transaction into the Transaction Table.
        '''
        cnx = mysql.connector.connect(user='root', password='Th3T3chBoy$',
                                      host='127.0.0.1',
                                      database='stockportfolio')

        product_id = self._get_ticker_id(input_ticker)

        mySql_insert_query = """INSERT INTO transaction (idtransaction, fk_idproduct_transaction, transactionTime, buySell, price) VALUES (null, %s, %s, true, %s)"""
        timestamp = self._get_current_time

        print('Timestamp:  ', timestamp)
        recordTuple = (str(product_id), timestamp, str(value))
        print('recordTuple', recordTuple)
        cursor = cnx.cursor()
        print('Executing....')
        cursor.execute(mySql_insert_query, recordTuple)
        cnx.commit()
        cursor.close()
        cnx.close()
        print('Success')
        return


    def run(self, interval = 600, max_iterations = 100):
        '''schedule the query for given interval'''
        schedule.every(interval).seconds.do(self.query)
        iterations = 0
        start = time.time()
        print("... running:  ", iterations)
        while interval < max_iterations:
            print('iteration:  ', iterations)
            schedule.run_pending()
            time.sleep(interval)
            iterations+=1

        print('.. complete in {} seconds'.format(time.time() - start))
        return

if __name__ == '__main__':

    api = BinanceAPI()
    print("...get_price")
    api.get_price("BTCUSDT")
    print("...query")
    api.query()

    #yahoo_api.query()
    #yahoo_api.run(interval = 10, max_iterations = 1440)
