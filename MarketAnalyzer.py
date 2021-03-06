#Python modules
import numpy as np
import pandas as pd
import time
from decimal import Decimal
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq
import functools
import matplotlib.pyplot as plt
import time
### Sofiat imports
#from singularity import *

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        runtime = time.time() - start
        print(f'Completed  {func.__name__!r}  in {runtime:.3f} sec')
        return response
    return wrapper_timer


class MarketAnalyzer():
    def __init__(self):
        self.params = {
                    'commission' : Decimal(0.075),
                    'timeFrames' : ['1m', '1h']
                    }
        return

    def Analyze(self):
        return


    def fee_threshold(fee = 0.075):
        """You must sell at this price to make ANY profit"""
        return (2 * fee)/(1 + fee)

    @classmethod
    def compute_signal(cls, main_frame, params = (9, 12, 26),
                    function = 'rolling'):
        frame = main_frame.copy()
        buy_signal  = params[0]
        fast_signal = params[1]
        slow_signal = params[2]

        if function == 'rolling':
            #print('computing rolling')
            frame['fast']   = frame['close'].rolling(window=fast_signal).mean()
            frame['slow']   = frame['close'].rolling(window=slow_signal).mean()
            frame['macd']   = frame['fast'] - frame['slow']
            frame['signal'] = frame['macd'].rolling(window=buy_signal).mean()

        elif function == 'exponential':
            #print('computing exponential')
            frame['fast']   = frame['close'].ewm(span = fast_signal, adjust=True).mean()
            frame['slow']   = frame['close'].ewm(span = slow_signal, adjust=True).mean()
            frame['macd']   = frame['fast'] - frame['slow']
            frame['signal'] = frame['macd'].ewm(span = buy_signal, adjust=True).mean()

        frame['delta']        = frame['macd'] - frame['signal']
        frame['d_delta']      = np.gradient(frame['delta'])
        frame['d_delta_var']  = np.sqrt(frame['d_delta'].rolling(window=20).var()[20:])
        frame['strength']     = np.divide(np.abs(frame['d_delta']), frame['d_delta_var'])
        return frame

    ################################################################################
    @classmethod
    def critical_index(cls, frame, use_variance=True):

        variance_condition = lambda delta, var : (np.abs(delta) > var ) if use_variance else [True] * len([delta])
        frame = frame[np.isfinite(frame['delta'])]

        left = np.array(frame['delta'])[:-1]
        right = np.array(frame['delta'])[1:]
        dp = list(np.sign(left * right))
        dp.insert(0,np.nan)  #Adds day to "approximate" / get frames equal lengths

        indices = frame[(np.array(dp) < 0.0) &  variance_condition(frame['d_delta'], frame['d_delta_var'])].copy()  #+/- 1 DAY
        indices['buysell']  = np.sign(indices['delta'])
        return indices

    ################################################################################



    def reoptimize(frame, SIGNAL_GRID, function = 'rolling', use_variance = True):
        start = time.time()
        MACD_ARRAY = [MACD_MATRIX(frame, params = ele,
                                    commission = 0.075,
                                    function=function) for ele in SIGNAL_GRID]
        MACD_GAINS = np.array(MACD_ARRAY)
        MAX_INDEX = np.where(MACD_GAINS == max(MACD_GAINS))[0][0]
        print('Time:   ', time.time() - start)
        print('Gain:   ', max(MACD_GAINS))

        return SIGNAL_GRID[MAX_INDEX], MACD_GAINS


    def MACD_MATRIX(frame, params = (9, 12, 26), commission = 0.075, function = 'exponential'):
        """ assume fast, slow, signal, MACD """

        """
        | date, price, side, delta, ...

        """
        frame = analyze_signals(frame, params, function)
        WORKING = frame['close'].values

        GAIN = np.divide(WORKING[1::2], WORKING[:-1:2]).prod()

        LEFT = np.divide(np.cumprod(WORKING[1:-2:2]), np.cumprod(WORKING[2:-1:2]))
        LEFT = np.insert(arr = LEFT, values=1., obj=0)

        RIGHT = WORKING[::2] + WORKING[1::2]

        FEE = commission * np.dot(LEFT, RIGHT)/100./WORKING[0]

        return (GAIN - FEE - 1.)*100.

    def analyze_signals(frame, params, function):
        working = frame.copy(deep=True)

        working = compute_signal(working, params, function)
        SIGNALS = critical_index(working)

        ##row/index of first buy
        ENTRY   = SIGNALS[SIGNALS['buysell'] > 0].index[0]
        EXIT    = SIGNALS[SIGNALS['buysell'] < 0].index[-1]
        ##strip the stuff before
        SIGNALS = SIGNALS.loc[ENTRY:EXIT]

        ## get the cycle indexes
        order = np.array(SIGNALS['buysell'])[1:] + np.array(SIGNALS['buysell'])[:-1]

        ##index the frame for cycles, including first buy.
        return SIGNALS.iloc[np.insert(arr = np.where(order == 0)[0] + 1, values=[0], obj=0)]

    @staticmethod
    def load_signal_grid(self):
        ## What if I left these completely free?..
        buy_signal_span  = np.arange(5, 15)
        fast_signal_span = np.arange(5, 30)
        slow_signal_span = np.arange(15, 55)


        signal_grid = np.meshgrid(buy_signal_span, fast_signal_span, slow_signal_span)
        buy_signal_array  = []
        fast_signal_array = []
        slow_signal_array = []

        fast_offset = 1
        slow_offset = 5

        for buy, fast, slow in zip(signal_grid[0].flatten(), signal_grid[1].flatten(), signal_grid[2].flatten()):
            if (buy + fast_offset < fast) and (fast + slow_offset < slow) :
                buy_signal_array.append(buy)
                fast_signal_array.append(fast)
                slow_signal_array.append(slow)

        SIGNAL_GRID = np.array([buy_signal_array, fast_signal_array, slow_signal_array]).T
        return SIGNAL_GRID


    #@timer
    def MACD_scenario(frame, buy_signal = 9, fast_signal = 12, slow_signal = 26,
                    commission = 0.075, function = 'rolling', verbose=False, use_variance=True):

        commission = commission / 100.
        frame   = compute_signal(frame, params = (buy_signal, fast_signal, slow_signal), function = function)
        #buy_signal, fast_signal, slow_signal

        buysell = critical_index(frame)

        variance_condition = lambda delta, var : (np.abs(delta) > var ) if use_variance else [True] * len([delta])
        ####################################################
        ### assume principal investment is $1.00
        principal = 1.00

        #-------------------------------------
        ## Interpolate the price
        ## locate the first buy-in
        buy_index = buysell[(buysell['buysell'] > 0) & variance_condition(buysell['d_delta'], buysell['d_delta_var'])]
        sell_index = buysell[(buysell['buysell'] < 0) & variance_condition(buysell['d_delta'], buysell['d_delta_var'])]

        try:
            #### SCENARIO
            ################################################################
            current_wallet = principal
            current_share  = 0.0
            num_trades     = 0
            fee            = 0.0
            print("-------------------------------------------------") if verbose else None
            #try:
            entry_index =  buy_index.index[ 0]
            last_index  = sell_index.index[-1]
            natural_gain   = float(buy_index['close'][entry_index]) / float(sell_index['close'][last_index])
            for i, row in buysell.loc[entry_index : last_index].iterrows():
                current_price = round(float(row['close']), 2) #price_function(row['index'])
                strength      = round(float(row['d_delta'] / row['d_delta_var']), 2)
                #print(price_function(row['index']), row['close'])

                if   (row['buysell'] < 0 ) and variance_condition(row['d_delta'], row['d_delta_var']): ## SELL
                    if current_share != 0:
                        #print('selling')
                        current_wallet += current_share * current_price
                        fee += (current_share * current_price) * commission
                        print('Selling @ $%8.2F|   Balance $%6.2F    |    DeltaVar: %2.2F'%(current_price, current_wallet, strength)) if verbose else None
                        current_share = 0
                        num_trades += 1


                elif (row['buysell'] > 0) and variance_condition(row['d_delta'], row['d_delta_var']): ## BUY
                    if current_wallet != 0:
                        #print('buying')
                        current_share = current_wallet / current_price
                        fee += (current_share * current_price) * commission
                        print('Buying  @ $%8.2F|                             DeltaVar: %2.2F'%(current_price, strength)) if verbose else None
                        current_wallet = 0
                        num_trades += 1

            #print(f'Selling {current_share} shares @ ${final_price}')
            percent_gain  = 100. * ((current_wallet - fee) - 1.)
            if verbose:
                print("-------------------------------------------------")
                print(f'Number of trades: {num_trades}')
                print(f'Wallet : ${current_wallet} | Fee : ${fee}')
                print(f'Percent gain: {percent_gain} | Fee: {fee}')
                print(f'Natural gain:  {natural_gain}')
            return percent_gain
        except Exception as e:
            return -np.inf



    def optimize(frame, SIGNAL_GRID, function = 'rolling', use_variance = True):
        start = time.time()
        MACD_ARRAY = [MACD_scenario(frame, buy_signal = ele[0], fast_signal=ele[1], slow_signal=ele[2],
                                    commission = 0.075, function=function, use_variance = use_variance) for ele in SIGNAL_GRID]
        MACD_GAINS = np.array(MACD_ARRAY)
        MAX_INDEX = np.where(MACD_GAINS == max(MACD_GAINS))[0][0]
        print('Time:   ', time.time() - start)
        print('Gain:   ', max(MACD_GAINS))

        return SIGNAL_GRID[MAX_INDEX], MACD_GAINS


    def format_frames(frame):
            try:
                frame['open_time'] = frame['open_time'].apply(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
                frame['close_time'] = frame['close_time'].apply(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
                frame['symbol'] = frame['symbol'].apply(lambda x : str(x))
            except:
                pass
            for column in ['open', 'high', 'volume', 'low', 'close',
                'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                'ignore']:
                try:
                    frame[column] = frame[column].apply(lambda x : float(x))
                except:
                    print(frame[column])

            return frame


def make_plot(frame, indices):
    """Visualizes data using matplotlib"""
    plt.rcParams['font.family'] = 'Times New Roman'
    fig = plt.figure(figsize=(6, 8))

    ax = []
    ax.append(plt.subplot(311))
    ax.append(plt.subplot(312, sharex = ax[0]))
    ax.append(plt.subplot(313, sharex = ax[1]))

    fig.subplots_adjust(hspace = 0.1)

    COLOR= {1 : "green",
            -1 : "red"}

    frame['count'] = np.arange(len(frame))

    MIN = min(frame.index)
    MAX = max(frame.index)


    ax[0].plot(frame.index, frame['close'], color='black', linewidth=0.75)
    ax[0].scatter(indices['count'], indices['close'], s=25,
            color = [COLOR[ele] for ele in indices['buysell']])

    ax[2].plot(frame.index, frame['signal'])
    ax[2].plot(frame.index, frame['macd'])

    ax[1].scatter(frame.index, frame['d_delta'], color='black', s=5)


    for i, row in indices.iterrows():
        [label.axvline(row['count'], linewidth=0.5, alpha=0.5,
        color = COLOR[row['buysell']]) for label in ax]


    ax[1].scatter(indices['count'], indices['d_delta'], s=20,
                    color=[COLOR[ele] for ele in indices['buysell']])


    DELTA_STD = np.std(indices['d_delta'])
    DELTA_MEAN = np.mean(indices['d_delta'])

    print(DELTA_STD, DELTA_MEAN)
    length = len(indices)

    ax[1].fill_between(frame['count'].iloc[10:],
                       -np.sqrt(frame['d_delta'].ewm(span= 20, adjust=False).var()[10:] ),
                       np.sqrt(frame['d_delta'].ewm(span= 20, adjust=False).var()[10:]),
                        alpha = 0.25, color = 'yellow')

    ax[1].fill_between(frame['count'].iloc[10:],
                       -np.sqrt(frame['d_delta'].rolling(window=20).var()[10:] ),
                       np.sqrt(frame['d_delta'].rolling(window=20).var()[10:]),
                        alpha = 0.25, color = 'grey')

                #.ewm(span = buy_signal, adjust=False).mean()

    for i in range(0, len(indices) - 1):
        row  = indices.iloc[i]
        price = row['close']
        if row['buysell'] == 1:
            print('------------------')
            print(price)
            print(price * (1 + fee_threshold(0.075)/100.))

            print(row['count'])
            print(indices.iloc[i+1]['count'])
            ax[0].fill_between([ row['count'], indices.iloc[i+1]['count'] ] ,
                                np.zeros(2) + price,
                                np.zeros(2) + price * (1 + fee_threshold(0.075)/100.),
                                color = 'orange', alpha=0.25)

    [label.axhline(0.0) for label in ax[1:]]


    ax[0].legend()

    [label.tick_params(direction = 'in', top=True, right=True) for label in ax]

    return fig, ax
