import numpy as np
import pandas as pd

def calculate_sma(prices,lookback=14):
    prices = pd.DataFrame(prices)
    sma = prices.cumsum()
    sma.values[lookback:] = (sma.values[lookback:] - sma.values[:-lookback]) / lookback
    sma.ix[:lookback] = np.nan
    return sma

# vectorize the price/SMA ratio
def calculate_price_sma_ratio(prices,lookback=14):
    prices = pd.DataFrame(prices)
    sma = prices.cumsum()
    sma.values[lookback:,:] = (sma.values[lookback:,:] - sma.values[:-lookback,:]) / lookback
    sma.ix[:lookback,:] = np.nan
    price_sma_ratio = prices / sma
    return price_sma_ratio

# vectorize the bollinger band
def calculate_bollinger_band(prices,lookback=14):
    prices = pd.DataFrame(prices)
    sma = calculate_sma(prices,lookback=lookback)
    rolling_std = prices.rolling(window=lookback,min_periods=lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (prices - bottom_band) / (top_band - bottom_band)
    return bbp

def calculate_full_bollinger_band(prices,lookback=14):
    prices = pd.DataFrame(prices)
    sma = calculate_sma(prices,lookback=lookback)
    rolling_std = prices.rolling(window=lookback,min_periods=lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bb_percentage = (prices - bottom_band) / (top_band - bottom_band)
    bb_bandwidth = (top_band - bottom_band) * 2 / (top_band + bottom_band)
    return bb_percentage, bb_bandwidth, top_band, bottom_band

# vectorize the rsi
def calculate_rsi(prices,lookback=14):
    prices = pd.DataFrame(prices)
    rsi = prices.copy()
    daily_rets = prices.copy()
    daily_rets.values[1:,:] = prices.values[1:,:] - prices.values[:-1,:]
    daily_rets.values[0,:] = np.nan
    up_rets = daily_rets[daily_rets>=0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets<0].fillna(0).cumsum()
    up_gain = prices.copy()
    up_gain.ix[:,:] = 0
    up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]
    down_loss = prices.copy()
    down_loss.ix[:,:] = 0
    down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]
    for day in range(len(prices)):
        # up_gain = daily_rets.ix[day-lookback+1:day+1,:].where(daily_rets >= 0).sum()
        # down_loss = -1 * daily_rets.ix[day-lookback+1:day+1,:].where(daily_rets < 0).sum()
        up = up_gain.ix[day,:]
        down = down_loss.ix[day,:]
        # rs = (up_gain / lookback) / (down_loss / lookback)
        rs = (up / lookback) / (down / lookback)
        rsi.ix[day,:] = 100 - (100 / (1 + rs))
    # rsi.ix[:lookback,:] = np.nan
    rsi[rsi == np.inf] = 100
    return rsi

# vectorize the Momentum
def calculate_momentum(prices, lookback=14):
    prices = pd.DataFrame(prices)
    momentum = prices.copy()
    momentum.values[lookback:,:] = prices.values[lookback:,:] - prices.values[:-lookback,:]
    momentum.values[:lookback,:] = np.nan
    return momentum