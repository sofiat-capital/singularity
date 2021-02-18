###############################################################################
#CREATE DATA-RELATIONAL MODEL USING SCHEMA DEFINITION LANGUAGE
###############################################################################
from sqlalchemy import  MetaData, Table, Column, create_engine, sql
from sqlalchemy.sql import select
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, DECIMAL, TINYINT, DATETIME
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, ForeignKey
from datetime import datetime, timedelta

#SoFIAT modules
from .base import BaseAPI
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import os
################################################################################
#Create SoFIAT DB classesz
################################################################################
class TableMixin(object):
    """Create MySQL database Metadata"""
    def __init__(self):
        self.metadata = MetaData()
        self.Category = Table('Category', self.metadata,
            Column('idCategory', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('name', VARCHAR(25), nullable=False),
            PrimaryKeyConstraint('idCategory', name='idCategory_pk'),
            mysql_engine="InnoDB"
            )

        self.Product = Table('Product', self.metadata,
            Column('idProduct', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('fk_idCategory_Product', INTEGER(11, unsigned=True), nullable=False),
            Column('ticker', VARCHAR(15), nullable=False),
            PrimaryKeyConstraint('idProduct', name='idProduct_pk'),
            ForeignKeyConstraint(['fk_idCategory_Product'],['Category.idCategory']),
            mysql_engine="InnoDB"
            )

        self.DayCandle = Table('DayCandle', self.metadata,
            Column('idDayCandle',INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('fk_idProduct_DayCandle', INTEGER(11, unsigned=True), nullable=False),
            Column('date', DATETIME()),
            Column('open', DECIMAL(20,12)),
            Column('hi', DECIMAL(20,12)),
            Column('low', DECIMAL(20,12)),
            Column('close',DECIMAL(20,12)),
            Column('volume', DECIMAL(20,12)),
            Column('numTrades', INTEGER(11, unsigned=True)),
            PrimaryKeyConstraint('idDayCandle', name='idDayCandle_pk'),
            ForeignKeyConstraint(['fk_idProduct_DayCandle'],['Product.idProduct']),
            mysql_engine="InnoDB"
            )

        self.OrderQueue = Table('OrderQueue', self.metadata,
            Column('idOrderQueue', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('fk_idProduct_OrderQueue', INTEGER(11, unsigned=True), nullable=False),
            Column('side', VARCHAR(25)),
            Column('timeCreated', DATETIME()),
            Column('price', DECIMAL(20,12)),
            Column('executed', TINYINT(4)),
            Column('type', VARCHAR(25)), #FOREIGN KEY NOW?
            PrimaryKeyConstraint('idOrderQueue', name='idOrderQueue_pk'),
            ForeignKeyConstraint(['fk_idProduct_OrderQueue'],['Product.idProduct']),
            mysql_engine="InnoDB"
            )

        self.BinanceOrder = Table('BinanceOrder', self.metadata,
            Column('fk_idOrderQueue_BinanceOrder', INTEGER(11, unsigned=True), primary_key=True, nullable=False),
            Column('fk_idProduct_BinanceOrder', INTEGER(11, unsigned=True), primary_key=True, nullable=False),
            Column('orderListId', INTEGER(11, unsigned=True), nullable=False),
            Column('transactTime', DATETIME(), nullable=False),
            Column('price', DECIMAL(20,12), nullable=False),
            Column('origQty', DECIMAL(20,12)),
            Column('executedQty', DECIMAL(20,12)),
            Column('cummulativeQuoteQty', DECIMAL(20,12)),
            Column('status', VARCHAR(15)),
            Column('timeInForce', VARCHAR(15)),
            Column('type', VARCHAR(8)),
            Column('side', VARCHAR(8)),
            ForeignKeyConstraint(['fk_idOrderQueue_BinanceOrder'],['OrderQueue.idOrderQueue']),
            ForeignKeyConstraint(['fk_idProduct_BinanceOrder'],['Product.idProduct']),
            mysql_engine="InnoDB"
            )

        self.BinanceFill = Table('BinanceFill', self.metadata,
            Column('idBinanceFill', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('fk_idOrderQueue_BinanceOrder_BinanceFill', INTEGER(11, unsigned=True), nullable=False),
            Column('price', DECIMAL(20,12), nullable=False),
            Column('qty', DECIMAL(20,12), nullable=False),
            Column('commission', DECIMAL(20,12)),
            Column('commissionAsset', VARCHAR(15)),
            PrimaryKeyConstraint('idBinanceFill', name='idBinanceFill_pk'),
            ForeignKeyConstraint(['fk_idOrderQueue_BinanceOrder_BinanceFill'],['BinanceOrder.fk_idOrderQueue_BinanceOrder']),
            mysql_engine="InnoDB"
            )

        self.Portfolio = Table('Portfolio', self.metadata,
            Column('idPortfolio', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('asOfDate', DATETIME(), nullable=False),
            Column('valuation', DECIMAL(20,12), nullable=False),
            Column('USD', DECIMAL(12,2)),
            Column('BTC', DECIMAL(20,12)),
            Column('ETH', DECIMAL(20,12)),
            Column('LTC', DECIMAL(20,12)),
            PrimaryKeyConstraint('idPortfolio', name='idPortfolio_pk'),
            mysql_engine="InnoDB"
            )

        #CHANGE 'GAINSTABLE' TO 'GAINS'
        self.Gains = Table('Gains', self.metadata,
            Column('idGains', INTEGER(11, unsigned=True), primary_key=True, nullable=False, autoincrement=True),
            Column('fk_idProduct_Gains', INTEGER(11), nullable=False),
            Column('symbol', VARCHAR(10), nullable=False),
            Column('cycleTime', DATETIME(), nullable=False),
            Column('gainPercent', DECIMAL(20,12), nullable=False),
            Column('gainAmount', DECIMAL(10,3), nullable=False),
            PrimaryKeyConstraint('idGains', name='idGains_pk'),
            ForeignKeyConstraint(['fk_idProduct_Gains'],['Product.idProduct']),
            mysql_engine="InnoDB"
            )


class DataBaseAPI(BaseAPI, TableMixin):
    """API for SoFIAT MySQL Database"""
    def __init__(self):
        """Import constructors explicitly (multiple inheritence?)"""
        BaseAPI.__init__(self)
        TableMixin.__init__(self)

        #Make connection to database
        self.keychain = {'mysql' : os.environ.get('mysql_key')}
        url = 'mysql+pymysql://root:{}@localhost/sofiat'.format(self.keychain.get('mysql'))

        #Create engine & connect
        self.engine = create_engine(url)
        self.engine.connect()
        return

    ############################################################################
    ### SELECT statements
    ############################################################################
    def GetProductTickers(self):
        """SELECT and return only ticker column"""
        connection = self.engine.connect()
        tickers = []
        statement = self.Product.select(self.Product)
        rows = connection.execute(statement)
        for row in rows:
            tickers.append(row.ticker)
        return tickers


    def GetBinanceOrderFills(self, symbol  = "ETHUSDT"):
        """SELECT and JOIN BinanceOrder & BinanceFill tables
        and then gather all data assocaited with symbol passed (ETHUSDT)"""
        connection = self.engine.connect()
        product_id = self._get_product_id(symbol)

        j = self.BinanceOrder.join(self.BinanceFill, self.BinanceOrder.c.fk_idOrderQueue_BinanceOrder == self.BinanceFill.c.fk_idOrderQueue_BinanceOrder_BinanceFill)
        statement = select([self.BinanceOrder, self.BinanceFill]).select_from(j).where(self.BinanceOrder.c.fk_idProduct_BinanceOrder == product_id)
        result = connection.execute(statement).fetchall()
        return result


    def GetPendingOrderQueue(self, delta):
        """SELECT newest order within OrderQueue table within time delta"""
        connection = self.engine.connect()
        #Used to cancel outdated orders
        start_time = datetime.now() - timedelta(seconds=delta)

        query = self.OrderQueue.select(self.OrderQueue).where(
                                        self.OrderQueue.c.executed == False,
                                        self.OrderQueue.c.timeCreated > start_time
                                        ).order_by(
                                        self.OrderQueue.c.timeCreated.desc(),
                                        )
        result = connection.execute(query).first()
        return result


    def UpdateOrderQueue(self, order):
        """Passed an Order within OrderQueue table -- updates execution column"""
        connection = self.engine.connect()
        query = self.OrderQueue.select(self.OrderQueue).where(self.OrderQueue.c.idOrderQueue == order.idOrderQueue).first()
        result = connection.execute(query)
        if result:
            result.executed = True
            return True
        return False


    ############################################################################
    ### INSERT statements
    ############################################################################
    def CreateProduct(self, productName, categoryName):
        """INSERT into Product table of SoFIAT Database"""
        connection = self.engine.connect()
        statement = self.Product.insert().values(
                        fk_idCategory_Product  =  self._get_category_id(categoryName),
                        ticker = productName)
        connection.execute(statement)
        self.log(f'Created Product:  {productName} - {categoryName}')
        return True


    def CreateCategory(self, name):
        """INSERT into Category table of SoFIAT Database"""
        connection = self.engine.connect()
        query = self.Category.insert().values(
                        name = name)
        result = connection.execute(query)
        self.log(f'Created Category:  {categoryName}')
        return True


    def InsertDayCandle(self, daycandles):
        """INSERT into DayCandle table of SoFIAT Database"""
        for i, candle in daycandles.iterrows():
            statement = self.DayCandle.insert().values(
                     fk_idProduct_DayCandle = self._get_product_id(candle['symbol']),
                     date   = candle['close_time'],
                     low    = float(candle['low']),
                     hi     = float(candle['high']),
                     open   = float(candle['open']),
                     close  = float(candle['close']),
                     volume = float(candle['volume']),
                     numTrades = int(candle['number_of_trades'])
                     )
            connection.execute(statement)
        self.log(f"Record inserted successfully into dayCandle {candle['symbol']}")
        return


    def InsertRealTime(self, symbol, price, time = None):
        """INSERT into RealTime table of SoFIAT Database"""
        connection = self.engine.connect()
        product_id = self._get_product_id(symbol)

        if not product_id:
            self.log(f"Product doesn't exist!:  {symbol}")
            return False
        if not time:
            time = self.current_time

        realtime = self.RealTime.insert().values(
                        fk_idProduct_RealTime = product_id,
                        observedPrice = price,
                        observedTime  = time,
                        )
        connection.execute(element)
        return True


    def InsertOrderQueue(self, **params):
        """INSERT order queue entry from BUY/SELL signal"""
        connection = self.engine.connect()

        #Associate passed ticker string with product ID
        product_id = self._get_product_id(params.get('symbol'))
        start_date = datetime.now() - timedelta(seconds = 60)

        #Is there an order of same currency, side, and within time Binance takes to update?
        query = self.OrderQueue.select(self.OrderQueue).where(
                    self.OrderQueue.fk_idProduct_OrderQueue == product_id,
                    self.OrderQueue.side == params['side'],
                    self.OrderQueue.timeCreated > start_date
                    )

        order = connection.execute(query).first()

        #If order exists -- close conneciton?
        if order:
            #maybe close connection?
            return False

        statement = self.OrderQueue.insert().values(
                      fk_idProduct_OrderQueue = product_id,
                      side        = params['side'],
                      timeCreated = params.get('timeCreated', datetime.now()),
                      price       = params.get('price')
                      )
        connection.execute(statement)
        self.log(f'Committed: Order {params.get("symbol")} - {params.get("side")} to OrderQueue')
        return True


    def InsertBinanceOrder(self, params):
        """ INSERT order from successful Binance order payload """
        connection = self.engine.connect()
        product_id = self._get_product_id(params.get('symbol'))

        #Data to be inserted into BinanceOrder table
        query = self.BinanceOrder.insert().values(
                            fk_idOrderQueue_BinanceOrder = int(params.get('clientOrderId')),
                            fk_idProduct_BinanceOrder    = product_id,
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
        connection.execute(query)
        self.log('Committed Binance Order')
        return True


    def InsertBinanceFills(self, params):
        """INSERT fills from successful Binance order payload"""
        connection = self.engine.connect()

        #Obtain idBinance order from BinanceOrder table payload
        idbinanceOrder = params.get('clientOrderId')

        #Ensure order exists in BinanceOrder (and therefore OrderQueue table)
        query = self.BinanceOrder.select(self.BinanceOrder).where(
                    self.BinanceOrder.c.fk_idOrderQueue_BinanceOrder == idbinanceOrder)
        binance_order = connection.execute(query).first()

        #If BinanceOrder doesn't exist (there will be no fills to create)
        if not binance_order:
            self.log(f'order {idbinanceOrder} does not exist!')

        #Iterates through indivdual fills of order
        fills = params.get('fills', [])
        for current_fill in fills:
            statement = self.BinanceFill.insert().values(
                fk_idOrderQueue_BinanceOrder_BinanceFill = idbinanceOrder,
                price = current_fill.get('price'),
                qty = current_fill.get('qty'),
                commission = current_fill.get('commission'),
                commissionAsset = current_fill.get('commissionAsset')
                )
            connection.execute(statement)
            print('Did thing')
        self.log('Committed Binance Fills')
        return True


    def InsertPortfolio(self, params):
        """ INSERT fills from successful Binance order payload """
        connection = self.engine.connect()
        statement = self.Portfolio.insert().values(
                asOfDate  = params.get('asOfDate', datetime.now()),
                valuation = params.get('valuation'),
                USD       = params.get('USD', 0.0),
                BTC       = params.get('BTC', 0.0),
                ETH       = params.get('ETH', 0.0),
                LTC       = params.get('LTC', 0.0)
                )
        result = connection.execute(statement)
        self.log(f"Committed: Portfolio Snapshots: {params.get('valuation')}")
        return True


    def InsertGainsTable(self, gains_frame):
        """INSERT computed gains from trades into gains table"""
        connection = self.engine.connect()

        #Iterate through fills passed in from Binance Order table
        for i, row in gains_frame.iterrows():
            #print(gains_frame['time'])
            print(row['time'].to_pydatetime(), type(row['time']))

            statement = self.Gains.select(self.Gains).where(
                                    self.GainsTable.c.symbol == row['symbol'],
                                    self.GainsTable.c.cycleTime == row['time'].to_pydatetime()
                                    )
            new_table = connection.execute(statement).first()

            #Insert gains for each fill of the Binance Order
            if new_table is None:
                statement = self.BinanceFill.insert().values(
                                symbol       = row['symbol'],
                                cycleTime    = row['time'].to_pydatetime(),
                                gainPercent  = row['gain[%]'],
                                gainAmount   = row['gain[$]'],
                                fk_idProduct_Gains = self._get_product_id(row['symbol'])
                                )
                result = connection.execute(statement)
        return True

    ############################################################################
    ### HELPER functions
    ############################################################################
    def _get_category_id(self, category_name):
        """Obtain given idCategory value when passed associated category string"""
        connection = self.engine.connect()
        query = self.Category.select(self.Category.c.idCategory).where(
                                            self.Category.c.name == category_name)
        result = connection.execute(query).first()
        if not result:
            self.log(f"Product ID {category_name} doesn't exist")
            return None
        return result.idCategory


    def _get_product_id(self, ticker):
        """Obtain given idProduct when given ticker"""
        connection = self.engine.connect()
        query = self.Product.select(self.Product.c.idProduct).where(self.Product.c.ticker == ticker)
        result = connection.execute(query).first()
        if not result:
            self.log(f"Ticker {ticker} doesn't exist")
            return None
        return result.idProduct


    def _get_product_ticker(self, product_id):
        """Return ticker when given product_id"""
        connection = engine.connect()
        query = self.Product.select(self.Product.c.ticker).where(self.Product.c.idProduct == product_id)
        result = connection.execute(query).first()
        if not result:
            self.log(f"Product ID {product_id} doesn't exist")
            return None
        return result.ticker


############################
###        Test
############################
if __name__ == '__main__':
    db_api = DataBaseAPI()
