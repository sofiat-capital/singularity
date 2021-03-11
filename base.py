# USED FOR COMMON METHODS IN BINANCE API HELPER CLASSES
import os, sys
import time
from .skype import SkypeBot
from datetime import datetime
from pyfiglet import Figlet



class BaseAPI(object):
    def __init__(self):
        self.skype = None

    def intro(self):
        self.clear()
        f = Figlet(font='slant')
        self.span_window()
        print(f.renderText('SoFIAT'))
        self.span_window()
        print('Authors:  Devin Whitten | Austin Stockwell')
        print('Email:    dev.sofiat@gmail.com')
        self.span_window()
        return

    def span_window(self, symbol = '-'):
        print(symbol * os.get_terminal_size().columns)
        return

    def clear(self):
        os.system("clear")
        return


    @property
    def current_timestamp(self):
        ''' CONVERTS MACHINE CODE IN msecs to "BINANCE FORMAT (NO DECIMAL))'''
        ''' INPUT: 1611106199.60748 --> 1611106199607'''
        ts = datetime.now().timestamp()
        return int(ts * 1000.)

    @staticmethod
    def from_timestamp(timestamp):
        ''' CONVERTS "BINANCE FORMAT (NO DECIMAL IN msecs to MACHINE CODE))'''
        ''' INPUT: 1611106199607 -->  1611106199.60748'''
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


    @staticmethod
    def date_to_timestamp(input_date):
        '''CONVERTS 'DATE FORMAT TO TIMESTAMP'''
        '''INPUT:  2021-01-19  -->  OUTPUT: 1611106199'''
        line = input_date.split('-')
        date = datetime(year=int(line[0]), month=int(line[1]), day=int(line[2]))
        return date.timestamp()



    @property
    def current_time(self):
        ''' Current time in human format
        '''
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp



    def log(self, msg="", flush=False, to_skype=False):
        output = '{} - {}: {}'.format(self.current_time, self.__class__.__name__, msg)
        if flush:
            print(output, end = '\r', flush=True)
            #sys.stdout.flush()
        else:
            print(output)
        if self.skype and to_skype:
            self.skype.send(output)
            pass
        return
