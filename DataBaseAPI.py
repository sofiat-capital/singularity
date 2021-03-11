'''
DATE   : 12/29/2021
AUTHORS: Devin Whitten & Austin Stockwell
EMAIL  :  dev.sofiat@gmail.com
SoFIAT Capital (All rights reserved)
'''
############################################################################
#System Modules
import os, sys
#Python Modules
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
from sqlalchemy.pool import NullPool
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
            self.Engine = create_engine(url, poolclass=NullPool)#pool_size=20, max_overflow=0, pool_recycle=10)
            self.Engine.connect()
            self.Session = sessionmaker()
            self.Session.configure(bind=self.Engine)
        except:
            self.log('Error connecting to database')
        self.base = automap_base()
        self.base.prepare(self.Engine, reflect=True)
        self.models = self.base.classes
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
        self.CandleStick  = self.engine.models.get('candleStick')
        self.Transaction  = self.engine.models.get('transaction')
        self.RealTime     = self.engine.models.get('realTime')
        self.BinanceOrder = self.engine.models.get('binanceOrder')
        self.BinanceFill  = self.engine.models.get('binanceFill')
        self.OrderQueue   = self.engine.models.get('orderQueue')
        self.Portfolio    = self.engine.models.get('portfolio')
        self.GainsTable   = self.engine.models.get('gainsTable')
        return

    @property
    def session(self):
        return self.engine.Session()

    def status(self):
        self.log(self.engine.Engine.pool.status())
################################################################################
    ############################################################################
    ### Insert FUNCTIONS
    ############################################################################
    def InsertCandleStick(self, candles):
        """INSERT into CandleStick table of SoFIAT Database"""
        session = self.engine.Session()

        for i, candle in candles.iterrows():
            ## make sure it's not there
            candle_query = session.query(self.CandleStick).filter(
                                self.CandleStick.closeTime == candle['close_time'],
                                self.CandleStick.openTime  == candle['open_time'],
                                self.CandleStick.interval  == candle['interval']).all()

            if not candle_query:
                element = self.CandleStick(fk_idproduct_candleStick = self._get_product_id(candle['symbol']),
                                         openTime    = candle['open_time'],
                                         closeTime   = candle['close_time'],
                                         low         = float(candle['low']),
                                         hi          = float(candle['high']),
                                         open        = float(candle['open']),
                                         close       = float(candle['close']),
                                         volume      = float(candle['volume']),
                                         numTrades   = int(candle['number_of_trades']),
                                         interval    = candle['interval']
                                       )
                session.add(element)
            else:
                pass
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
        return True


    def InsertOrderQueue(self, **params):
        """INSERT order queue entry from BUY/SELL signal"""
        #Create a session
        session = self.engine.Session()

        #Obtains a product_id given the symbol passed
        product_id = self._get_product_id(params.get('symbol'))

        print('Order queue: '.format(params))

        #Ensures current time is not still within same binance sampling window
                                                                                #BINANCE SAMPLING RATE / WINDOW
        start_date = datetime.now() - timedelta(seconds = params.get('interval', 30 * 60))

        #Query Order Queue table for desired product within the sampling window
        orders = session.query(self.OrderQueue).filter(
                            self.OrderQueue.fk_idproduct_orderQueue == product_id,
                            self.OrderQueue.side == params['side'],
                            self.OrderQueue.executed == False,
                            self.OrderQueue.timeCreated > start_date).all()

        #Cancel order if looking at same Binance sampling window as last order
        if len(orders) > 0:
            for order in orders:
                print(order.side, order.price, order.executed, order.timeCreated)

            session.close()
            return False

        #Build the order
        order = self.OrderQueue(fk_idproduct_orderQueue = product_id,
                                      side        = params['side'],
                                      timeCreated = params.get('timeCreated', datetime.now()),
                                      price       = params.get('price'),
                                      type        = params.get('type', 'MARKET')
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
            self.log(f'order {idbinanceOrder} does not exist!')
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
        self.log(f"committed: Binance Order Fills: {binance_order.fk_idorderQueue_binanceOrder}")
        session.close()
        return True


    def InsertPortfolio(self, params):
        """INSERT fills from successful Binance order payload"""
        ''' idportfolio, asOfDate, valuation, USD, BTC, ETH, LTC '''
        session =  self.engine.Session()
        portfolio = self.Portfolio(
                asOfDate  = params.get('asOfDate', datetime.now()),
                valuation = params.get('valuation'),
                USD       = params.get('USD', 0.0),
                BTC       = params.get('BTC', 0.0),
                ETH       = params.get('ETH', 0.0),
                LTC       = params.get('LTC', 0.0)
                    )
        session.add(portfolio)
        session.commit()
        self.log(f"Committed: Portfolio Snapshots: {params.get('valuation')}")
        session.close()


    def InsertGainsTable(self, gains_frame):
        session =  self.engine.Session()

        for i, row in gains_frame.iterrows():
            #print(gains_frame['time'])
            print(row['time'].to_pydatetime(), type(row['time']))
            new_table = session.query(self.GainsTable).filter(
                                    self.GainsTable.symbol == row['symbol'],
                                    self.GainsTable.cycleTime == row['time'].to_pydatetime()
                                    ).one_or_none()


            if new_table is None:   ## uf the gainstable doesn't exist
                new_table = self.GainsTable(
                        symbol       = row['symbol'],
                        cycleTime    = row['time'].to_pydatetime(),
                        gainPercent  = row['gain[%]'],
                        gainAmount   = row['gain[$]'],
                        fk_idproduct_gainsTable = self._get_product_id(row['symbol'])
                        )
                session.add(new_table)
        session.commit()
        session.close()
        return

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
    def GetProductTable(self):
        """SELECT"""
        session = self.engine.Session()
        product_list = session.query(self.Product).all()
        session.close()
        return product_list

    def GetCandleStickFrame(self, interval, symbol='ETHUSDT'):
        """SELECT from CandleSticks table of SoFIAT Database"""
        #IF columns isn't provided in param list, return all columns in table
        columns = ['open_time', 'close_time', 'open', 'hi', 'low', 'close', 'volume', 'numTrades', 'interval']
        session =  self.engine.Session()
        product_id = self._get_product_id(ticker = symbol)
        day_candles = session.query(self.CandleStick).filter(
                                    self.CandleStick.fk_idproduct_candleStick == product_id).all()
        reformat = []
        for candle in list(set(day_candles)):
            reformat.append([candle.openTime,
                             candle.closeTime,
                             candle.open,
                             candle.hi,
                             candle.low,
                             candle.close,
                             candle.volume,
                             candle.numTrades,
                             candle.interval])

        frame = pd.DataFrame(data = reformat,
                             columns = columns)

        frame['open_time']  = pd.to_datetime(frame['open_time'])
        frame['close_time'] = pd.to_datetime(frame['close_time'])

        frame = frame.set_index('close_time').sort_index()
        session.close()
        return frame


    def GetPendingOrderQueue(self, delta, type='MARKET'):
        """SELECT newest OrderQueue row within a defined time delta"""
        session =  self.engine.Session()
        delta = timedelta(seconds=delta)
        order = session.query(self.OrderQueue).filter(
                                                    self.OrderQueue.executed == False,
                                                    self.OrderQueue.type == type,
                                                    ).order_by(self.OrderQueue.timeCreated.desc()).first()
        if order is None or (datetime.now() - order.timeCreated > delta):
            ####   stale order condition
            return None
        session.close()
        return order

    def UpdateOrderQueue(self, order):
        """SELECT newest OrderQueue row within a defined time delta"""
        session = self.engine.Session()

        order = session.query(self.OrderQueue).filter(
                                                self.OrderQueue.idorderQueue == order.idorderQueue
                                                ).one_or_none()
        if order:
            order.executed = True
            session.add(order)
            session.commit()
            session.close()
            return True
        session.close()
        return False




    ############################################################################
    ### HELPER FUNCTIONS
    ############################################################################
    def _get_product_id(self, ticker):
        """Helper function -- Returns Product ID when given Ticker Symbol"""
        session = self.engine.Session()
        product = session.query(self.Product).filter(self.Product.ticker == ticker).first()
        if not product:
            self.log("Product {} doesn't exist".format(ticker))
            session.close()
            return None
        session.close()
        return product.idproduct


    def _get_symbol_from_id(self, product_id):
        """Helper function -- Returns Product ID when given Ticker Symbol"""
        session = self.engine.Session()
        product = session.query(self.Product).filter(self.Product.idproduct == product_id).first()
        if not product:
            self.log("Product ID {} doesn't exist".format(product_id))
            session.close()
            return None
        session.close()
        return product.ticker


    ############################################################################
    ### USER
    ############################################################################
    def GetBinanceOrderFills(self, symbol  = "ETHUSDT"):
        """SELECT and JOIN binanceOrder & binanceFill tables"""
        session = self.engine.Session()
        product_id = self._get_product_id(symbol)

        #FULLY JOIN binanceOrder & binaceFills tables
        orders = session.query(self.BinanceOrder).join(self.BinanceFill).filter(
                            self.BinanceOrder.fk_idproduct_binanceOrder == product_id
                            ).order_by(self.BinanceOrder.transactTime.desc()).all()
        return orders

    def GetProductTickers(self):
        """SELECT and return only ticker column"""
        session = self.engine.Session()
        tickers = []
        rows = session.query(self.Product).all()
        for row in rows:
            tickers.append(row.ticker)
        session.close()
        return tickers

################################################################################
if __name__ == '__main__':
    db = DataBaseAPI()
