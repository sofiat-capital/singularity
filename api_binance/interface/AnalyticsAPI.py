import pandas as pd
from .base_api import BaseAPI
from .DataBaseAPI import DataBaseAPI
from .BinanceAPI import BinanceAPI

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

class AnalyticsAPI(BaseAPI):

    def __init__(self):
        BaseAPI.__init__(self)
        self.log("initializing AnalyticsAPI")
        self.BinanceAPI = BinanceAPI()

        return


    def MovingAverage(self, symbol='ETHUSDT', rate = 50):

        frame = self.BinanceAPI.CandleStick(symbol, interval = '1d', limit = 100)
        print(frame)

        frame['date'] = pd.to_datetime(frame['date'], format='%m%d%Y')
        frame = frame.set_index('date')

        return frame
