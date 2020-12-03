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
