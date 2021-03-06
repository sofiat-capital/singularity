'''
DATE   : 12/29/2021
AUTHORS: Devin Whitten & Austin Stockwell
EMAIL  :  dev.sofiat@gmail.com
SCOPE: Stats and values of SoFIAT Portfolio
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
        self.symbols = self.DataBaseAPI.GetProductTickers()
        return
################################################################################
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


    def GetUSDTotal(self):
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


    def ComputeGainsTable(self):
        """Computes cycle gains on pall SoFIAT products"""
        #List holds the gains of each product (then INSERTED into GainsTable)
        gains_frame = []

        #Loop through each symbol in ProductTable
        for symbol in self.symbols:
            orders = self.DataBaseAPI.GetBinanceOrderFills(symbol = symbol)

            #Intitialize gains frame that will be appended with CYCLE GAINS
            gain = []

            #Initialize entry and exit totals
            entry_total = 0
            exit_total  = 0

            #Iterating throught JOINED TABLE (binanceOrder & binanceFill)
            for order in orders:
                side = order.side
                fills = order.binancefill_collection
                fill_frame = pd.DataFrame([[fill.qty, fill.price] for fill in fills],
                                            columns = ['qty', 'price'])

                if  side == 'BUY':
                    #Assign newest entry for BUY price of all fills to entry_total
                    entry_total = np.array(fill_frame['qty'] * fill_frame['price'], dtype=float).sum()
                    pass

                elif side == 'SELL':
                    #Assign newest entry for SELL price of all fills to exit_total
                    exit_total  = np.array(fill_frame['qty'] * fill_frame['price'], dtype=float).sum()

                    #Calculate % gains / montetary gain of Cycle
                    percent_gain  = 100.* (np.divide(exit_total , entry_total) - 1.)
                    monetary_gain = (exit_total - entry_total)

                    #Append cycle's performance metrics to gain frame
                    gain.append([symbol, order.transactTime,  percent_gain, monetary_gain])

                frame = pd.DataFrame(gain, columns=['symbol', 'time', 'gain[%]', 'gain[$]'])
            #Add products gains to grain_frame
            gains_frame.append(frame.iloc[1:])

            #gains_frame = pd.concat(gains_frame)
        gains_frame = pd.concat(gains_frame)
        self.DataBaseAPI.InsertGainsTable(gains_frame)
        return gains_frame


    def PerformanceReport(self, to_skype=True):
        """ Logs the current USD Valuation of Portfolio,
            appends portfolio table with current quantities
            logs portfolio gains since runtime
        """
        current_value = self.PortfolioManager.GetUSDTotal()
        gain = (current_value/self.initial_balance - 1) * 100
        self.span_window()
        self.log(f'Current Balance:  ${round(current_value,2)}\nRuntime Gain:  {round(gain,2)}%', to_skype=to_skype)

        #Returns a list of dictionaries (rows of info about each financial product)
        balances = self.PortfolioManager.wallet.get('balances')

        #Convert list of dictionaries above into a panda frame for ease of use
        balancesFrame = pd.DataFrame(balances)
        #Turns index column into asset column
        balancesFrame.index = balancesFrame.asset

        #Search through dataframe for the values associated with each product
        #Cast data in frame to floats to perform totals on each product
        BNB = np.array(balancesFrame.loc['BNB'][['free', 'locked']], dtype=float).sum()
        BTC = np.array(balancesFrame.loc['BTC'][['free', 'locked']], dtype=float).sum()
        ETH = np.array(balancesFrame.loc['ETH'][['free', 'locked']], dtype=float).sum()
        LTC = np.array(balancesFrame.loc['LTC'][['free', 'locked']], dtype=float).sum()

        #Sum up all USDT Tethers(create single value for portfolio table)
        USD = 0
        for ele in ['USD', 'USDT', 'USDC']:
            USD += np.array(balancesFrame.loc[ele][['free', 'locked']], dtype=np.float64).sum()

        self.DataBaseAPI.InsertPortfolio(
                {'asOfDate'  : datetime.now(),
                 'valuation' : float(current_value),
                 'USD'       : float(USD),
                 'BTC'       : float(BTC),
                 'ETH'       : float(ETH),
                 'LTC'       : float(LTC),
                 'BNB'       : float(BNB)
                })
        return



    def CashOut(self):
        """ Emergency market exit to USD
            trades all nonzero balances to USD
        """
        return
