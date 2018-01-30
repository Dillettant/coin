import os, sys
sys.path.append("../")
from HuobiService import *

import json
import numpy as np
import pandas as pd

symbols = pd.read_json(json.dumps(get_symbols()["data"]))
symbols = symbols.sort_values(by="quote-currency", axis=0)

def query_symbols(quote_currency = "btc"):
    group = symbols.loc[symbols["quote-currency"]==quote_currency]
    query_symbols = []
    for each in group["base-currency"].tolist():
        query_symbols.append(str(each + quote_currency))
    return query_symbols

btc_query_symbols = query_symbols(quote_currency = "btc")
eth_query_symbols = query_symbols(quote_currency = "eth")
usdt_query_symbols = query_symbols(quote_currency = "usdt")

acctid = get_accounts()["data"][0]["id"]

def load_balance():
    balance = pd.read_json(json.dumps(get_balance(acct_id=acctid)["data"]["list"]))
    return balance

# choose the first symbol
sim_data = get_kline(symbol=btc_query_symbols[0], period="1min", size=2000)
sim_data = json.dumps(sim_data["data"])

sim_data = pd.read_json(sim_data)
# use the close prices as the price
close_prices = sim_data["close"]

def plot_figure(df = close_prices, color = ["blue"]):
    import matplotlib.pyplot as plt
    # Plot stock prices with a custom title and meaningful axis labels.
    ax = df.plot(title="demo", fontsize=12)
    ax.set_color_cycle(color)
    ax.set_xlabel("time stamp")
    ax.set_ylabel("closed prices")
    plt.show()

'''indicators'''
# vectorize the sma
def calculate_sma(prices,lookback=14):
    sma = prices.cumsum()
    sma.values[lookback:] = (sma.values[lookback:] - sma.values[:-lookback]) / lookback
    sma.ix[:lookback] = np.nan
    return sma
sma = calculate_sma(close_prices, lookback=14)
# plot_figure(df = pd.concat([close_prices, sma],axis=1),\
#     color = ["yellow","red"])
# print pd.concat([close_prices, sma],axis=1)

def save_data(df, file_name):
    if not os.path.exists("./data"):
        os.makedirs("./data")
    np.save("./data/{}.npy".format(file_name), sma)

save_data(close_prices, "close_prices")

def read_data(file_name):
    return np.load("./data/{}.npy".format(file_name))
rg_data = read_data("close_prices")

plot_figure(df = pd.DataFrame(rg_data))

trade_book = []
order_book = []