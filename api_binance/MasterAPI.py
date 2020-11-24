# PYTHON MODULES
import schedule
# USER DEFINED MODULES
from interface.DataBaseAPI import DataBaseAPI
from interface.base_api import BaseAPI
from interface.BinanceAPI import BinanceAPI
from interface.AnalyticsAPI import AnalyticsAPI


class MasterAPI(BaseAPI):
    def __init__(self):
        self.log('initializing MasterAPI')
        BaseAPI.__init__(self)

        self.DataBaseAPI = DataBaseAPI()
        self.BinanceAPI = BinanceAPI()
        self.AnalyticsAPI = AnalyticsAPI()



        return

    ############################################################################
    def run(self, interval=10):
        schedule.every(interval).seconds.do(self.query)

        while True:
            self.log('running... ')
            schedule.run_pending()
            time.sleep(interval)
        return
    ############################################################################



##################ñ##########################################################
#MAIN CODE MAIN CODE MAIN CODE MAIN
############################################################################
if __name__ == '__main__':
    api = MasterAPI()  #Creates object (instance of BinanceAPI class)
    api.AnalyticsAPI.MovingAverage()
    #api.AnalyticsAPI.MovingAverage()
