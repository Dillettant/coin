import numpy as np
import pandas as pd
import os, sys
sys.path.append("../")
from indicators import *

def read_data(file_name):
    return np.load("./data/{}.npy".format(file_name))

prices = read_data("close_prices")

'''indicators
sma:
sma_ratio:
bollinger_band:
full_bollinger_band:
rsi:
momentum:
'''
sma = calculate_price_sma_ratio(prices)
bbp = calculate_bollinger_band(prices)
rsi = calculate_rsi(prices)
momentum = calculate_momentum(prices)

trades = []
holdings = {0:0}
lookback = 14
sma_threshold = 0.05
rsi_oversold = 30
rsi_overbought = 60
momentum_threshold = 0
bbp_threshold = 0.5

sym = 0
for day in range(lookback+1, len(prices)):
    # stock may be oversold. Index does not appear to be oversold
    # we should long the stock
    if (sma.ix[day,sym] < 1-sma_threshold) \
    and (bbp.ix[day,sym] < 0) \
    and (rsi.ix[day,sym] < rsi_oversold) \
    and (momentum.ix[day,sym] < 0):
    # and (rsi.ix[day,"SPY"] > self.rsi_oversold) \
        if holdings[sym] < 1000:
            holdings[sym] += 1000
            trades.append([prices[day],sym,"BUY",1000])

    # stock may be overbought. Index does not appear to be overbought
    # we should short the stock
    elif (sma.ix[day,sym] > 1+sma_threshold) \
    and (bbp.ix[day,sym] > 1) \
    and (rsi.ix[day,sym] > rsi_overbought) \
    and (momentum.ix[day,sym] > 0):
    # and (rsi.ix[day,"SPY"] < self.rsi_overbought) \
        if holdings[sym] > -1000:
            holdings[sym] -= 1000
            trades.append([prices[day],sym,"SELL",1000])

    elif (sma.ix[day,sym] >= 1) \
    and (sma.ix[day-1,sym] < 1) \
    and (holdings[sym] > 0) \
    and (momentum.ix[day,sym] > 0):
        # crossed sma upwards and holding long. Close long position
        # we should sell the stock if we're holding the stock
        holdings[sym] = 0
        trades.append([prices[day],sym,"SELL",1000])
    elif (sma.ix[day,sym] <=1) \
    and (sma.ix[day-1,sym] > 1) \
    and (holdings[sym] < 0) \
    and (momentum.ix[day,sym] < 0):
        # crossed sma downwards and holding short. Close short position
        # we should sell the stock if we're holding the stock
        holdings[sym] = 0
        trades.append([prices[day],sym,"BUY",1000])

print trades