import os, sys
import numpy as np
import time
from datetime import datetime
from skpy import Skype


class SkypeBot(object):
    def __init__(self):
        SKYPE_USER = os.environ.get('skype_user')
        SKYPE_PASS = os.environ.get('skype_pass')
        SKYPE_ID   = os.environ.get('skype_chat_id')
        self.sk = Skype(SKYPE_USER, SKYPE_PASS)
        self.chats = self.sk.chats.recent()
        try:
            self.ch = self.sk.chats.chat(list(self.chats.keys())[0])
            self.send('SkypeBot Re-entered chat')
            self.get_fortune()
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


    def get_fortune(self):
        fortunes = ["A little caution outflanks a large cavalry.",
		    'A man is not old until regrets take the place of dreams.', \
	            'Do or do not, there is no try', \
                    'All those moments will be lost in time,\n like tears in rain.', \
                    'Opportunities multiply as they are seized.',\
		    'I don\'t like sand. It\'s coarse and rough and irritating and it gets everywhere.']
        return self.send("SkypeBot says : {}".format(np.random.choice(fortunes)))


if __name__ == "__main__":
    skypeboy = SkypeBot()
