###############################################################################
#CREATE DATA-RELATIONAL MODEL USING SCHEMA DEFINITION LANGUAGE
###############################################################################
from sqlalchemy import  MetaData, Table, Column, create_engine
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, DECIMAL, TINYINT, DATETIME
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, ForeignKey





################################################################################
#Create SoFIAT DB classes
################################################################################
class DataBaseAPI():#(BaseAPI):
    """API for SoFIAT MySQL Database"""
    def __init__(self):
        self.engine = create_engine(f"mysql+pymysql://root:Th3T3chBoy$@localhost/sofiat_test?charset=utf8mb4")
        #Use connect() method of the Engine object to returns an object Connection type
        self.engine.connect()


    ##################################################
    #Create MySQL Table abstractions
    ##################################################
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
            Column('origQtY', DECIMAL(20,12)),
            Column('executedQty', DECIMAL(20,12)),
            Column('cummulativeQuoteQty', DECIMAL(20,12)),
            Column('status', VARCHAR(15)),
            Column('timeInForce', VARCHAR(15)),
            Column('type', VARCHAR(8)),
            Column('side', VARCHAR(8)),
            ForeignKeyConstraint(['fk_idOrderQueue_BinanceOrder'],['Product.idProduct']),
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
        return


    ############################################################################
    ### SELECT statements
    ############################################################################
    def GetPendingOrderQueue(self, delta):
        """SELECT newest order within OrderQueue table within time delta"""
        connection = engine.connect()
        query = OrderQueue.select(OrderQueue).where(
                                        OrderQueue.c.executed == False).order_by(
                                        OrderQueue.timeCreated.desc(),
                                        ).first()
        result = connection.execute(query)

        #IF stale order condition
        delta = timedelta(seconds=delta)
        if result is None or (datetime.now() - OrderQueue.timeCreated > delta):
            return None
        row = result.fetchone()
        return row


    ############################################################################
    ### INSERT statements
    ############################################################################
    def InsertBinanceOrder(self, params):
        """INSERT order from successful Binance order payload"""
        connection = self.engine.connect()
        product_id = self._get_product_id(params.get('symbol'))
        if not product_id:
            self.log(f"Product doesn't exist! Creating Product for:  {symbol}")
            self.CreateProduct(productName = symbol, categoryName = 'Cryptocoin')
            self.log(f'Created product for {symbol}')
            product_id = self._get_product_id(params.get('symbol'))

        #Data to be inserted into BinanceOrder table
        query = self.BinanceOrder.insert().values(
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
        r = connection.execute(query)
        self.log(f'committed: Binance Order {query.fk_idorderQueue_binanceOrder} - {query.status}')
        return True


    def CreateProduct(self, productName, categoryName):
        """INSERT into Product table of SoFIAT Database"""
        connection = self.engine.connect()
        query = self.Product.insert().values(
                        fk_idCategory_Product  =  self._get_category_id(categoryName),
                        ticker = productName)
        print(self._get_category_id(categoryName))
        # product = connection.execute(query)

        return True

        '''
                #IF CAN NOT CREATE PRODUCT...
                if not product:
                    #CREATE CATEGORY
                    category = self.CreateCategory(categoryName)
                    print(category.idCategory)
                    #Re-try Creation of Product
                    product = self.Product.insert().values(
                            fk_idCategory_product = category.idCategory,
                            ticker = productName)
                    product = connection.execute(query)

                # self.log(f'Committed new Product field:  {product}')
        '''




    def CreateCategory(self, name):
        """INSERT into Category table of SoFIAT Database"""
        connection = engine.connect()
        query = self.Category.insert.values(
                        name = name)
        category = connection.execute(query)

        if not result:
            connection = engine.connect()
            result = self.Category(name = name)
            session.add(category)
            session.commit()
            self.log(f'Committed new Category field:  {category}')
        else:
            self.log('Category {} exists'.format(name))
        session.close()
        return category



    def UpdateOrderQueue(self, order):
        """Passed an Order within OrderQueue table -- updates execution column"""
        connection = engine.connect()
        query = OrderQueue.select(OrderQueue).where(OrderQueue.c.idOrderQueue == order.idOrderQueue).one_or_none()
        connection = engine.connect()
        result = connection.execute(query)
        if query:
            OrderQueue.c.executed = True
            return True
        return False






    ############################################################################
    ### HELPER functions
    ############################################################################
    def _get_category_id(self, category_name):
        """Obtain given idCategory value when passed associated category string"""
        connection = self.engine.connect()
        query = self.Category.select(self.Category.c.idCategory).where(self.Category.c.name == category_name)

        #Execute query; Look at First Row; Return only idCategory
        try:
            result = connection.execute(query)
            row = result.fetchone()
            idCategory = (row[self.Category.c.idCategory])
        except exc.SQLAlchemyError:
            print("SQL ERROR!")
            # self.log(f"Category name {category_name} doesn't exist!")
        return idCategory


    def _get_product_id(self, ticker):
        """Obtain given idProduct when given ticker"""
        connection = engine.connect()
        query = self.Product.select(self.Product.c.idProduct).where(self.Product.c.ticker == ticker)
        result = connection.execute(query)
        if not result:
            self.log(f"Ticker {ticker} doesn't exist")
            return None
        row = result.fetchone()
        idProduct = (row[Product.c.idProduct])
        return idProduct


    def _get_product_ticker(self, product_id):
        """Return ticker when given product_id"""
        connection = engine.connect()
        query = self.Product.select(self.Product.c.ticker).where(self.Product.c.idProduct == product_id)
        result = connection.execute(query)
        if not result:
            self.log(f"Product ID {product_id} doesn't exist")
            return None
        row = result.fetchone()
        ticker = (row[self.Product.c.ticker])
        return ticker



############################
#Test
############################
DataBaseAPI = DataBaseAPI()
DataBaseAPI._get_category_id('Cryptocoin')

###CREATE PRODUCT WORKS IF CATEGORY EXISTS -- START WITH testing ON
###WHEN CATEGORY DOES NOT EXIST!

'''
        super().__init__()
        self.log('INITIALIZING API and CONNECTING TO DATABASE (v3.0)')

        self.keychain = {'mysql_key' : os.environ.get('mysql_key')}
        try:
            url = 'mysql+pymysql://root:{}@localhost/sofiat'.format(self.keychain.get('mysql'))
            self.Engine = create_engine(url, poolclass=NullPool)
            self.Engine.connect()
            self.Session = sessionmaker()
            self.Session.configure(bind=self.Engine) #NECESSARY?
        except:
            self.log('Error connecting to database')
'''
