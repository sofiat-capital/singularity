# USED FOR COMMON METHODS IN BINANCE API HELPER CLASSES
import time
from datetime import datetime

from pyfiglet import Figlet

class BaseAPI(object):
    def __init__(self):
        return

    def intro(self):
        f = Figlet(font='slant')
        print(f.renderText('SoFiat'))
        return

    @property
    def current_time(self):
        ''' Current time in human format
        '''
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    @property
    def current_timestamp(self):
        ''' Current time in milliseconds
        '''
        ts = time.time()
        return int(ts * 1000.)


    @staticmethod
    def from_timestamp(timestamp):
        return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')


    def log(self, msg=""):
        print('{} - {}: {}'.format(self.current_time, self.__class__.__name__, msg))
        return
