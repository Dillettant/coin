from HuobiUtil import *

'''
Market data API
'''

# get KLine
def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: {1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# get market depth
def get_depth(symbol, type):
    """
    :param symbol:
    :param type: { percent10, step0, step1, step2, step3, step4, step5 }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}

    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)


# get trade detail
def get_trade(symbol):
    """
    :param symbol: { ethcny }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)


# get Market Detail 24hour tv
def get_detail(symbol):
    """
    :param symbol: { ethcny }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)

# querl all the symbol trades
def get_symbols():
    """
    :return:
    """
    url = MARKET_URL + '/v1/common/symbols'
    params = {}
    return http_get_request(url, params)

'''
Trade/Account API
'''
def get_accounts():
    """
    :return:
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)


# get current balance
def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """
    if not acct_id:
        try:
            accounts = get_accounts()
            acct_id = ACCOUNT_ID = accounts['data'][0]['id']
        except BaseException as e:
            print 'get acct_id error.%s' % e
            acct_id = ACCOUNT_ID

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)


# create and place an order
def send_order(amount, source, symbol, _type, price=0):
    """
    :param amount:
    :param source: if margin is required, please add 'margin-api' in params source
    :param symbol:
    :param _type: {buy-market:_, sell-market:_, buy-limit:_, sell-limit:_}
    :param price:
    :return:
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print 'get acct_id error.%s' % e
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


# withdrawl
def cancel_order(order_id):
    """
    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)


# query the order
def order_info(order_id):
    """
    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


# query the detials of an order
def order_matchresults(order_id):
    """

    :param order_id:
    :return:
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


# query current orders, history orders
def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol:
    :param states: {pre-submitted , submitted , partial-filled , partial-canceled , filled , canceled }
    :param types:  {buy-market: _, sell-market:_, buy-limit:_, sell-limit:_}
    :param start_date:
    :param end_date:
    :param _from:
    :param direct: {prev ,next }
    :param size:
    :return:
    """
    params = {'symbol': symbol,
              'states': states}

    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/orders'
    return api_key_get(params, url)


# query current trades, historical trades
def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol:
    :param types: {buy-market:_, sell-market:_, buy-limit:_, sell-limit: _}
    :param start_date:
    :param end_date:
    :param _from:
    :param direct: {prev,next}
    :param size:
    :return:
    """
    params = {'symbol': symbol}

    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/matchresults'
    return api_key_get(params, url)


# withdrawl
def withdraw(address, amount, currency, fee=0, addr_tag=""):
    """
    :param address_id:
    :param amount:
    :param currency:btc, ltc, bcc, eth, etc ...
    :param fee:
    :param addr_tag:
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {'address': address,
              'amount': amount,
              "currency": currency,
              "fee": fee,
              "addr-tag": addr_tag}
    url = '/v1/dw/withdraw/api/create'

    return api_key_post(params, url)

# cancel withdrawl
def cancel_withdraw(address_id):
    """

    :param address_id:
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

    return api_key_post(params, url)

if __name__ == '__main__':
    print get_symbols()