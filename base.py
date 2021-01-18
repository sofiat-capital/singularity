# USED FOR COMMON METHODS IN BINANCE API HELPER CLASSES
import os, sys
import time
from .skype import SkypeBot
from datetime import datetime
from pyfiglet import Figlet


class BaseAPI(object):
    def __init__(self, to_skype = False):
        if to_skype:
            self.skype = SkypeBot()
        else:
            self.skype = None
        return

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
        ''' Current time in milliseconds
        '''
        ts = time.time()
        return int(ts * 1000.)


    @staticmethod
    def from_timestamp(timestamp):
        return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def to_timestamp(input_date):
        '''YYYY-MM-DD'''
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


    def log(self, msg="", flush=False, to_slack=False):
        output = '{} - {}: {}'.format(self.current_time, self.__class__.__name__, msg)
        if flush:
            print(output, end='\r')
            #sys.stdout.flush()
        else:
            print(output)
        if self.skype and to_slack:
            self.skype.send(output)
        return
