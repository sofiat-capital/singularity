#Python Modules
import os, sys
import numpy as np
import pandas as pd
import datetime
from sqlalchemy import (create_engine, MetaData, Column,
        Integer, String, Table)
from datetime import datetime, timedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import SchemaItem
from sqlalchemy.types import TypeEngine
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
import pprint
#SoFIAT Modules
from .base import BaseAPI
############################################################################
class SQLEngine(BaseAPI):
    """Creates SQLEngine (Connection) to Database w/SQLALCHEMY"""
    def __init__(self):
        super().__init__()
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
        self.log('Initializing SQL Engine')
        return


class DataBaseAPI(BaseAPI):
    """API for SoFIAT MySQL Database"""
    def __init__(self):
        super().__init__()
        self.log('initializing DataBaseAPI')
        self.keychain = {'mysql_key' : os.environ.get('mysql_key')}
        self.engine = SQLEngine()

        ### SQL Alchemy Models
        self.Category     = self.engine.models.get('category')
        self.Product      = self.engine.models.get('product')
        self.DayCandle    = self.engine.models.get('dayCandle')
        self.Transaction  = self.engine.models.get('transaction')
        self.RealTime     = self.engine.models.get('realTime')
        self.BinanceOrder = self.engine.models.get('binanceOrder')
        self.BinanceFill  = self.engine.models.get('binanceFill')
        self.OrderQueue   = self.engine.models.get('orderQueue')
        return


################################################################################
    ############################################################################
    ### Insert FUNCTIONS
    ############################################################################
    def InsertDayCandle(self, daycandles):
        """INSERT into DayCandle table of SoFIAT Database"""
        session = self.engine.Session()
        for i, candle in daycandles.iterrows():
            element = self.DayCandle(fk_idproduct_dayCandle = self._get_product_id(candle['symbol']),
                                     date   = candle['close_time'],
                                     low    = float(candle['low']),
                                     hi     = float(candle['high']),
                                     open   = float(candle['open']),
                                     close  = float(candle['close']),
                                     volume = float(candle['volume']),
                                     numTrades = int(candle['number_of_trades'])
                                   )
            session.add(element)
        self.log('Record inserted successfully into dayCandle {}'.format(candle['symbol']))
        session.commit()
        session.close()
        return


    def InsertRealTime(self, symbol, price, time = None):
        """INSERT into RealTime table of SoFIAT Database"""
        session = self.engine.Session()
        product_id = self._get_product_id(symbol)
        if not product_id:
            self.log("Product doesn't exist!:  {}".format(symbol))
            return False
        if not time:
            time = self.current_time
        realtime = self.RealTime(
                        fk_idproduct_realTime = product_id,
                        observedPrice = price,
                        observedTime  = time,
                        )
        session.add(realtime)
        session.commit()
        session.close()
        #self.log('committed: {} - {}'.format(symbol, time))
        session.close()
        return True


    def InsertOrderQueue(self, **params):
        """INSERT order queue entry from BUY/SELL signal"""
        session = self.engine.Session()
        product_id = self._get_product_id(params.get('symbol'))

        order = self.OrderQueue(fk_idproduct_orderQueue = product_id,
                                      side        = params['side'],
                                      timeCreated = params.get('timeCreated', datetime.now()),
                                      price       = params.get('price', None),
                                      quantity    = params.get('quantity', None),
                                      timeFilled  = params.get('timeFilled', None)
                                      )

        session.add(order)
        session.commit()
        self.log(f'committed: Order {params.get("symbol")} - {params.get("side")} to OrderQueue')
        session.close()
        return True


    def InsertBinanceOrder(self, params):
        """INSERT order from successful Binance order payload"""
        session =  self.engine.Session()
        product_id = self._get_product_id(params.get('symbol'))
        if not product_id:
            self.log(f"Product doesn't exist! Creating Product for:  {symbol}")
            self.CreateProduct(productName = symbol, categoryName = 'cryptocoin')
            self.log(f'Created product for {symbol}')
            product_id = self._get_product_id(params.get('symbol'))


        ### Create the binanceOrder
        binance_order = self.BinanceOrder(
                            fk_idorderQueue_binanceOrder = int(params.get('clientOrderId')),
                            fk_idproduct_binanceOrder    = product_id,
                            orderListId                  = params.get('orderListId'),
                            transactTime                 = self.from_timestamp(params.get('transactTime')/1000),
                            price                        = params.get('price'),
                            origQty                      = params.get('origQty'),
                            executedQty                  = params.get('executedQty'),
                            cummulativeQuoteQty          = params.get('cummulativeQuoteQty'),
                            status                       = params.get('status'),
                            timeInForce                  = params.get('timeInForce'),
                            type                         = params.get('type'),
                            side                         = params.get('side')
                        )
        session.add(binance_order)
        session.commit()
        self.log(f'committed: Binance Order {binance_order.fk_idorderQueue_binanceOrder} - {binance_order.status}')
        session.close()
        return True


    def InsertBinanceFills(self, params):
        """INSERT fills from successful Binance order payload"""
        session =  self.engine.Session()
        idbinanceOrder = params.get('clientOrderId')
        binance_order = session.query(self.BinanceOrder).filter(
                    self.BinanceOrder.fk_idorderQueue_binanceOrder == idbinanceOrder).one_or_none()

        if not binance_order:
            self.log('order {} does not exist!'.format(idbinanceOrder))
        fills = params.get('fills')

        ''' fk_idorderQueue_binanceOrder_binanceFill, price, qty, commission, commissionAsset '''

        for current_fill in fills:
            session.add(self.BinanceFill(
                                fk_idorderQueue_binanceOrder_binanceFill = idbinanceOrder,
                                price = current_fill.get('price'),
                                qty =   current_fill.get('qty'),
                                commission = current_fill.get('commission'),
                                commissionAsset = current_fill.get('commissionAsset')
                        )
            )
        session.commit()
        self.log('committed: Binance Order Fills: {}'.format(binance_order.idbinanceOrder))
        session.close()
        return True


    ############################################################################
    ### CREATE STATEMENTS
    ############################################################################
    def CreateCategory(self, name):
        """INSERT into Category table of SoFIAT Database"""
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
        """INSERT into Product table of SoFIAT Database"""
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


    ############################################################################
    ### SELECT STATEMENTS (Accessors)
    ############################################################################
    def GetDayCandleFrame(self, symbol='ETHUSDT', columns = None):
        """SELECT from DayCandles table of SoFIAT Database"""
        #IF columns isn't provided in param list, return all columns in table
        columns = ['date','open', 'hi', 'low', 'close', 'volume', 'numTrades']
        session =  self.engine.Session()
        product_id = self._get_product_id(ticker = symbol)
        day_candles = session.query(self.DayCandle).filter(
                            self.DayCandle.fk_idproduct_dayCandle == product_id).all()
        reformat = []
        for candle in list(set(day_candles)):
            reformat.append([candle.date,
                             candle.open,
                             candle.hi,
                             candle.low,
                             candle.close,
                             candle.volume,
                             candle.numTrades])
        frame = pd.DataFrame(data = reformat,
                             columns = columns)
        frame['date'] = pd.to_datetime(frame['date'], format='%Y-%m-%d')
        frame = frame.set_index('date').sort_index()
        return frame


    def GetPendingOrderQueue(self, delta):
        """SELECT newest OrderQueue row within a defined time delta"""
        session = self.engine.Session()
        delta = timedelta(seconds=delta)
        order = session.query(self.OrderQueue).filter(self.OrderQueue.executed == False).order_by(self.OrderQueue.timeCreated.desc()).first()
        if (datetime.now() - order.timeCreated > delta) or order is None:
            ####   stale order condition
            return None
        return order



    def GetRealTime(self, start_time, end_time = None, symbol='ETHUSDT'):
        """PRECONDITION: (Start TIMESTAMPOBJ, End TIMESTAMP OBJ, Symbol)"""
        """SELECT from RealTime table of SoFIAT Database"""
        session =  self.engine.Session()
        product_id = self._get_product_id(symbol)

        #If no max_date is provided, assume CURRENT is max_date
        if end_time is None:
            end_time = self.current_time

        #SELECT a window from RealTime table
        session.flush(self.RealTime)
        realtime = session.query(self.RealTime).filter(
                            self.RealTime.fk_idproduct_realTime == product_id,
                            self.RealTime.observedTime.between(start_time, end_time)
                            ).order_by(
                            self.RealTime.observedTime).all()

        session.close()
        return realtime

    def _get_product_id(self, ticker):
        """Helper function -- Returns Product ID when given Ticker Symbol"""
        session = self.engine.Session()
        product = session.query(self.Product).filter(self.Product.ticker == ticker).first()
        if not product:
            self.log("Product {} doesn't exist".format(ticker))
            return None
        session.close()
        return product.idproduct





################################################################################
    '''
    def GetOrderQueue(self):
        """ BinanceMaster.py utilizes to pass orders to Binance Endpoint  """
        session =  self.engine.Session()
        #columns = ['1','2']

        #Creates SELECT statement in SQLAlchemy (Primarily for testing???)
        if filled is None:
            order_queue = session.query(self.OrderQueue).order_by(
                    self.OrderQueue.timestamp.asc()).all()
        else:
            order_queue = session.query(self.OrderQueue).filter(
                    self.OrderQueue.filled == filled
                    ).order_by(self.OrderQueue.timestamp.asc()).all()
        session.close()
        return order_queue if order_queue else None
        '''
