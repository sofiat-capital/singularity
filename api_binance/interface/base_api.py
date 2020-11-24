# USED FOR COMMON METHODS IN BINANCE API HELPER CLASSES
import time
from datetime import datetime
class BaseAPI(object):
    def __init__(self):
        return

    @property
    def current_time(self):
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    @staticmethod
    def from_timestamp(timestamp):
        return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')


    def log(self, msg=""):
        print('{} - {}: {}'.format(self.current_time, self.__class__.__name__, msg))
        return
