'''
DATE   : 12/29/2021
AUTHORS: Devin Whitten & Austin Stockwell
EMAIL  :  dev.sofiat@gmail.com
SoFIAT Capital (All rights reserved)
'''
################################################################################
#SoFIAT modules
from singularity.base import BaseAPI
from singularity import DataBaseAPI
from singularity import BinanceAPI
#Python modules
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime
################################################################################
class PortfolioManager(BaseAPI):
    """Keeps track of current state of BinanceAccounts"""
    def __init__(self ):
        #self.DataBaseAPI = DataBaseAPI()
        self.BinanceAPI  = BinanceAPI()
        self.DataBaseAPI = DataBaseAPI()
        self.skype = None
        self.log('Initialized PortfolioManager')
        return


    def GetBalance(self, symbol = None):
        """Return account balance"""
        self.wallet = self.BinanceAPI.AccountInfo()
        #If we are passed a valid SYMBOL
        if symbol:
            balance = None
            for row in self.wallet.get('balances'):
                if row['asset'].upper() == symbol.upper():
                    balance = row
                    self.log(f"Your balance  of {balance.get('free')} is...")
            return Decimal(balance.get('free')) if balance else None
            self.log(f" Balance {self.wallet['balance']} Time {datetime.now()}")

        return self.wallet.get('balances')

################################################################################

    def GetUSDTotal(self):
        ##symbol = ['BTC', 'ETH', 'LTC']
        """ Computes total USD value of portfolio"""
        self.GetBalance()
        USD_TOTAL = 0
        for row in self.wallet.get('balances'):
            symbol  = row['asset']
            balance = float(row['free']) + float(row['locked'])
            if 'USD' in symbol:
                USD_TOTAL += balance
                continue
            balance = float(row['free']) + float(row['locked'])
            price = self.BinanceAPI.CurrentAveragePrice(symbol = symbol + "USD").get('price') if balance else 0.0
            USD_TOTAL += float(price) * balance

        return USD_TOTAL


    def ComputeGainsTable(self, symbol = 'BTCUSDT'):
        orders = self.DataBaseAPI.GetBinanceOrderFills()
        #print(len(orders))
        print(orders)

        #Intitialize gains table that will be appended with CYCLE GAINS
        gain = []
        print("------------------------")
        entry_total = 0
        exit_total = 0
        #Iterating throught JOINED TABLE ()
        for order in orders:

            side = order.side
            fills = order.binancefill_collection

            fill_frame = pd.DataFrame([[fill.qty, fill.price] for fill in fills],
                                        columns = ['qty', 'price'])
            #####################
            if  side == 'BUY':
                print(' BUYING')
                entry_total = np.array(fill_frame['qty'] * fill_frame['price'], dtype=float).sum()
                pass

            elif side == 'SELL':
                print(' Selling')

                exit_total  = np.array(fill_frame['qty'] * fill_frame['price'], dtype=float).sum()
                percent_gain = 100.* (np.divide(exit_total , entry_total) - 1.)
                monetary_gain = (exit_total - entry_total)

                gain.append([order.transactTime,  percent_gain, monetary_gain ])
            #####################
        return pd.DataFrame(gain, columns=['time', 'gain[%]', 'gain[$]'])


        '''

            fill_frame = pd.DataFrame([[fill.price, fill.qty] for fill in fills], columns = ['price', 'qty'])
            fill_frame['total'] = float(fill_frame['qty'] * fill_frame['price'])

            print(side, "---------", fill_frame['total'])

        return fill_frame
        '''



    def CashOut(self):
        """ Emergency market exit to USD
            trades all nonzero balances to USD
        """
        return
