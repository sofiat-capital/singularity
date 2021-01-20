import os, sys
import time
from datetime import datetime
from skpy import Skype


class SkypeBot(object):
    def __init__(self):
        SKYPE_USER = os.environ.get('skype_user', 'dev.sofiat@gmail.com',)
        SKYPE_PASS = os.environ.get('skype_pass', 'Th3T3chBoy$')
        SKYPE_ID   = os.environ.get('skype_chat_id', '19:ecfeb38d376c463489f76d1bdd3fee75@thread.skype')
        self.sk = Skype(SKYPE_USER, SKYPE_PASS)
        self.chats = self.sk.chats.recent()
        try:
            self.ch = self.sk.chats.chat(list(self.chats.keys())[0])
            self.send('SkypeBot Re-entered chat')
        except:
            self.ch = self.sk.chats.create(['live:.cid.df297e22cac21507', 'live:devinwhitten2014'])
            self.send('SkypeBot Re-initializing chat')
        return

    def _init_chat(self):
        chats = self.sk.chats.recent()

    @property
    def current_time(self):
        ''' Current time in human format
        '''
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    def send(self, msg):
        self.ch.sendMsg('{}'.format(msg))
