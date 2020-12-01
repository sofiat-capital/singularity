import os
import numpy as np
from .base_api import BaseAPI

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from alembic.autogenerate import compare_metadata

from alembic.migration import MigrationContext
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy.schema import SchemaItem
from sqlalchemy.types import TypeEngine
from sqlalchemy import (create_engine, MetaData, Column,
        Integer, String, Table)
from sqlalchemy.orm import sessionmaker
import pprint

import os, sys


# CREATES SQL ENGINE (CONNECTION) TO DATABASE WITH SQLALCHEMY
class SQLEngine(BaseAPI):
    def __init__(self):
        self.keychain = {'mysql' : os.environ.get('mysql_key')}

        try:
            url = 'mysql+pymysql://root:{}@localhost/sofiat'.format(self.keychain.get('mysql'))
            self.Engine = create_engine(url)
            self.Engine.connect()

            self.Session = sessionmaker()
            self.Session.configure(bind=self.Engine)

        except:
            self.log('Error connecting to database')

        self.base = automap_base()
        self.base.prepare(self.Engine, reflect=True)
        self.models = self.base.classes

        self.log('initializing SQL Engine')
        return


#
class DataBaseAPI(BaseAPI):
    def __init__(self):
        BaseAPI.__init__(self)
        self.log('initializing DataBaseAPI')
        self.keychain = {'mysql_key' : os.environ.get('mysql_key')}

        self.engine = SQLEngine()


        ### Models
        self.Category    = self.engine.models.get('category')
        self.Product     = self.engine.models.get('product')
        self.DayCandle   = self.engine.models.get('dayCandle')
        self.Transaction = self.engine.models.get('transaction')
        self.RealTime    = self.engine.models.get('realTime')


        return

    ############################################################################
    ### Insert FUNCTIONS
    ############################################################################
    def InsertDayCandle(self, daycandles):
        '''Precondition: daycandles is the result of self.kline
        '''
        session = self.engine.Session()

        for i, candle in daycandles.iterrows():

            element = self.DayCandle(fk_idproduct_dayCandle = self._get_product_id(candle['symbol']),
                                     date   = candle['close_time'],
                                     low    = float(candle['low']),
                                     hi     = float(candle['high']),
                                     open   = float(candle['open']),
                                     close  = float(candle['close']),
                                     volume = float(candle['volume']),
                                     numtrades = int(candle['number_of_trades'])
                                   )

            session.add(element)

        self.log('Record inserted successfully into dayCandle {}'.format(candle['symbol']))

        session.commit()
        session.close()
        return

    # ENTERS DATA INTO TRANSACTION TO TRACK TRADE HISTORY
    def InsertTransaction(self, input_ticker, buy_sell, price, quantity):
        session = self.engine.Session()
        timestamp = self.current_time
        product_id = self._get_product_id(input_ticker)
        if not product_id:
            self.log('No Product for {}'.format(input_ticker))
            return None

        transaction = self.Transaction(fk_idproduct_transaction = product_id,
                         transactionTime          = timestamp,
                         buySell                  = buy_sell,
                         price                    = price,
                         quantity                 = quantity)

        session.add(transaction)
        session.commit()

        self.log('Success')
        session.close()
        return


    def InsertRealTime(self, symbol, price, time = None):
        session = self.engine.Session()

        product_id = self._get_product_id(symbol)
        if not product_id:
            self.log("Product doesn't exist!:  {}".format(symbol))
            return

        if not time:
            time = self.current_time

        realtime = self.RealTime(
                        fk_idproduct_realTime = product_id,
                        observedPrice = price,
                        observedTime  = time,
                        )
        session.add(realtime)
        session.commit()
        self.log('committed: {} - {}'.format(symbol, time))

        return

    ############################################################################
    ### HIDDEN FUNCTIONS
    ############################################################################
    # OBTAINS VALUE STORED IN DATABASE ASSOCIATED WITH TICKER PASSED

    def CreateCategory(self, name):
        session = self.engine.Session()
        category = session.query(self.Category).filter(self.Category.name == name).first()

        if not category:  ### doesn't exist
            category = self.Category(name = name)
            session.add(category)
            session.commit()
            self.log('Committed new Category field:  {}'.format(category))

        else:
            self.log('Category {} exists'.format(name))

        session.close()
        return category




    def CreateProduct(self, productName, categoryName):
        session = self.engine.Session()
        product = session.query(self.Product).filter(self.Product.ticker == productName).first()

        if not product:  ## if product == None (doesn't exists)
            category = self.CreateCategory(categoryName)
            product = self.Product(ticker = productName,
                                   fk_idcategory_product = category.idcategory)

            session.add(product)
            session.commit()
            self.log('Committed new Product field:  {}'.format(product))

        else:
            self.log('Product {} exists'.format(product))

        session.close()
        return product



    def _get_product_id(self, ticker):
        session = self.engine.Session()

        product = session.query(self.Product).filter(self.Product.ticker == ticker).first()

        if not product:
            self.log("Product {} doesn't exist".format(ticker))
            return None

        session.close()
        return product.idproduct
