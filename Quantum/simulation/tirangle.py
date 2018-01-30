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

