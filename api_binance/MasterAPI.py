# PYTHON MODULES

from apscheduler.schedulers.background import BlockingScheduler

# USER DEFINED MODULES
from interface.DataBaseAPI import DataBaseAPI
from interface.base_api import BaseAPI
from interface.BinanceAPI import BinanceAPI
from interface.AnalyticsAPI import AnalyticsAPI


class MasterAPI(BaseAPI):
    def __init__(self):
        self.log('initializing MasterAPI')
        BaseAPI.__init__(self)

        # SoFIAT "Moules"
        self.DataBaseAPI = DataBaseAPI()
        self.BinanceAPI = BinanceAPI()
        self.AnalyticsAPI = AnalyticsAPI()

        return

    ############################################################################
    def test(self):
        self.log('test')
        return

    def run(self):
        # Python
        self.log('initializing BackgroundScheduler()')
        self.Scheduler = BlockingScheduler()

        #######
        self.log('adding job')
        self.Scheduler.add_job(self.realtime, 'interval', seconds = 1)

        self.log(self.Scheduler.print_jobs())

        self.log('running')
        self.Scheduler.start()

    ############################################################################
    ## USER DEFINED
    ############################################################################
    def realtime(self, **params):

        self.BinanceAPI.SymbolPriceTicker(symbol = 'BTCUSDT')
        self.DataBaseAPI.InsertRealTime(symbol = 'BTCUSDT',
                                        price = self.BinanceAPI.response.get('price'))

##################ñ##########################################################
#MAIN CODE MAIN CODE MAIN CODE MAIN
############################################################################
if __name__ == '__main__':
    api = MasterAPI()  #Creates object (instance of BinanceAPI class)
#    api.run()
    TEST_API_ORDER = {
        'symbol'     : 'BTCUSDT',
        'side'       : 'BUY',
        'type'       : 'MARKET',
        'quantity'   : 1,
        'recvWindow' : 5000,
        'timestamp'  : api.current_timestamp
        }

    TEST_ORDER = {
    "symbol"                   : "BTCUSDT",
    "idbinanceOrder"           :  1,
    "fk_idproduct_binanceOrder":  1,
    "orderListId"               : -1,
    "clientOrderId"            : 'TEST',
    "transactTime"             : api.current_time,
    "price"                    : 10.0,
    "origQty"                  : 9.99,
    "executedQty"              : 9.99,
    "cummulativeQuoteQty"      : 9.99,
    "status"                   : "OPEN",
    "timeInForce"              : "TEST TIME",
    "type"                     : "MARKET",
    "side"                     : "BUY"
    }

    ORDER_RESPONSE = {
      "symbol": "BTCUSDT",
      "orderId": 1,
      "orderListId": -1,
      "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
      "transactTime": 1507725176595,
      "price": "0.00000000",
      "origQty": "10.00000000",
      "executedQty": "10.00000000",
      "cummulativeQuoteQty": "10.00000000",
      "status": "FILLED",
      "timeInForce": "GTC",
      "type": "MARKET",
      "side": "SELL",
      "fills": [
        {
          "price": "4000.00000000",
          "qty": "1.00000000",
          "commission": "4.00000000",
          "commissionAsset": "USDT"
        },
        {
          "price": "3999.00000000",
          "qty": "5.00000000",
          "commission": "19.99500000",
          "commissionAsset": "USDT"
        },
        {
          "price": "3998.00000000",
          "qty": "2.00000000",
          "commission": "7.99600000",
          "commissionAsset": "USDT"
        },
        {
          "price": "3997.00000000",
          "qty": "1.00000000",
          "commission": "3.99700000",
          "commissionAsset": "USDT"
        },
        {
          "price": "3995.00000000",
          "qty": "1.00000000",
          "commission": "3.99500000",
          "commissionAsset": "USDT"
        }
      ]
    }

    ORDER_RESPONSE['idbinanceOrder'] = 1


    #api.DataBaseAPI.InsertBinanceOrder(TEST_ORDER)
    #api.DataBaseAPI.InsertBinanceFills(ORDER_RESPONSE)
