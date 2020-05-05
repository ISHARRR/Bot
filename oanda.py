from oandapyV20 import API
from pandas import DataFrame
from oandapyV20.contrib.requests import (
    MarketOrderRequest,
    TakeProfitDetails,
    StopLossDetails,
    TrailingStopLossOrderRequest,
    TrailingStopLossDetails
)

import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import json
import requests
import time
import oandapyV20.endpoints.pricing as pricing


# account authenticator returing access_token and accountid
def authenticator():
    access_token="ace07448fdbcddf1d24c76db4f654abd-0673bb236877d296d74b63fef2d9be08"
    accountID = "101-004-14591208-001"

    return accountID, access_token

accountID, access_token = authenticator()

# api access key
client = oandapyV20.API(access_token=access_token)
api = oandapyV20.API(access_token=access_token)

# requesting data
r = accounts.AccountSummary(accountID)
client.request(r)
# saving the response into a dataframe
response = DataFrame.from_dict(r.response)


def get_balance():
    return (response.loc['balance' , 'account'])

def get_margin_available():
    return (response.loc['marginAvailable' , 'account'])

def get_commission():
    return (response.loc['commission' , 'account'])

def get_open_trade_count():
    return (response.loc['openTradeCount' , 'account'])

def get_current_price(instrument):
    # passing arguments
    params ={"instruments": instrument}
    # places request
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv = api.request(r)
    # BS ways of naigating json
    res = r.response['prices']
    df = DataFrame.from_dict(res, orient='columns')
    df = df.loc[0, 'closeoutBid']
    # returing the current price ask to 4 decimal places
    return ("{:.{}f}".format(float(df), 4))


def create_order(instrument):
    # current price
    current_price = get_current_price(instrument)
    # self explanitpry
    STOP_LOSS = float(current_price) - 0.0050
    TAKE_PROFIT = float(current_price) + 0.0050
    TRAILING_STOP_LOSS = TrailingStopLossDetails(distance=0.0050)

    # The orderspecs
    mktOrder = MarketOrderRequest(
        instrument = instrument,
        units=1000,
        takeProfitOnFill=TakeProfitDetails(price=TAKE_PROFIT).data,
        stopLossOnFill=StopLossDetails(price=STOP_LOSS).data,
        trailingStopLossOnFill=TRAILING_STOP_LOSS.data
    )

    # print("Market Order specs: \n{}".format(json.dumps(mktOrder.data, indent=4)))

    # create the OrderCreate request
    r = orders.OrderCreate(accountID, data=mktOrder.data)

    try:
        # create the OrderCreate request
        rv = api.request(r)
    except oandapyV20.exceptions.V20Error as err:
        print(r.status_code, err)

    else:
        # print(json.dumps(rv, indent=2))
        try:
            data = DataFrame.from_dict(rv['orderCancelTransaction'], orient = 'index')
            status = data.loc['type', 0]
            reason = data.loc['reason', 0]
            id = data.loc['id', 0]
            print('Order status:', status +'\n'+ 'Reason:', reason +'\n'+ 'Trade ID:', id)
        except KeyError:
            # KeyError to determin catch error raised by json return of 'orderCancelTransaction' instead of 'orderFillTransaction'
            data = DataFrame.from_dict(rv['orderFillTransaction'], orient = 'index')
            status = data.loc['type', 0]
            id = data.loc['id', 0]
            print('Order status:', status +'\n'+ 'Trade ID:', id)


create_order('EUR_USD')
