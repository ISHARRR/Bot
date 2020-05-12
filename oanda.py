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
    token="ace07448fdbcddf1d24c76db4f654abd-0673bb236877d296d74b63fef2d9be08"
    accountID = "101-004-14591208-001"

    return accountID, token

accountID, token = authenticator()

# api access key
client = oandapyV20.API(access_token=token)
api = oandapyV20.API(access_token=token)

# requesting data
r = accounts.AccountSummary(accountID)
client.request(r)
# saving the response into a dataframe
response = DataFrame.from_dict(r.response)


def get_balance():
    return (response.loc['balance' , 'account'])


def get_pl():
    return (response.loc['pl' , 'account'])


def get_margin_available():
    return (response.loc['marginAvailable' , 'account'])


def get_commission():
    return (response.loc['commission' , 'account'])


def get_open_trade_count():
    return (response.loc['openTradeCount' , 'account'])


def get_instruments():
    accountID, token = authenticator()
    client = oandapyV20.API(access_token=token)

    r = accounts.AccountInstruments(accountID=accountID)
    rv = client.request(r)

    with open('instrument.txt', 'w') as outfile:
        json.dump(rv, outfile, indent=2)


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
    return float("{:.{}f}".format(float(df), 4))


def unit_amount(instrument, risk_percentage, buyorsell):
    current_price = get_current_price(instrument)
    leverage = 30
    balance = get_balance()
    risk_percentage = risk_percentage

    unit_size = (float(balance) * float(leverage)) * float(risk_percentage)
    unit_amount = float(unit_size) * float(current_price)

    if buyorsell == 'SELL':
        unit_amount = unit_amount * - 1
    elif buyorsell == 'BUY':
        unit_amount = unit_amount
    else:
        raise ValueError('Please enter BUY or SELL')

    return float((round(unit_amount)))


def pip_value(instrument, risk_percentage, buyorsell):
    CURRENT_PRICE = get_current_price(instrument)
    UNIT_AMOUNT = unit_amount(instrument, risk_percentage, buyorsell)
    pip = float(0.0001)

    pip_value = (pip/CURRENT_PRICE) * UNIT_AMOUNT
    return round(pip_value, 2)


def risk_management(instrument, risk_percentage, profit_ratio, loss_ratio, trailing_ratio, buyorsell):
    UNIT_AMOUNT = unit_amount(instrument, risk_percentage, buyorsell)
    PIP_VALUE = pip_value(instrument, risk_percentage, buyorsell)
    CURRENT_PRICE = get_current_price(instrument)
    pip = 0.0001

    if buyorsell == 'BUY':
        pip_gain = float(((risk_percentage * 100)/PIP_VALUE) * profit_ratio)
        pip_loss = (float(((risk_percentage * 100)/PIP_VALUE) * loss_ratio)) * -1
        pip_trailing = (float(((risk_percentage * 100)/PIP_VALUE) * trailing_ratio))
    elif buyorsell == 'SELL':
        pip_gain = float(((risk_percentage * 100)/PIP_VALUE) * profit_ratio)
        pip_loss = abs((float(((risk_percentage * 100)/PIP_VALUE) * loss_ratio)))
        pip_trailing = abs((float(((risk_percentage * 100)/PIP_VALUE) * trailing_ratio)))

    take_profit = round((pip_gain * pip), 4)
    stop_loss = round((pip_loss * pip), 4)
    trailing_stop = round((pip_trailing * pip), 4)

    take_profit_price = CURRENT_PRICE + take_profit
    stop_loss_price = CURRENT_PRICE + stop_loss
    # trailing stop is distnace therefore always positive
    trailing_stop_distance = trailing_stop

    return take_profit_price, stop_loss_price, trailing_stop_distance, risk_percentage


def create_order(instrument, risk_percentage, buyorsell):
    UNIT_AMOUNT = unit_amount(instrument, risk_percentage, buyorsell)
    # sets take profit and trailing stop loss
    TAKE_PROFIT_PRICE, STOP_LOSS_PRICE, TRAILING_STOP_DISTANCE, RISK_PERCENTAGE = risk_management(instrument, 0.1, 2, 1, 1, buyorsell)
    OPEN_TRADE_COUNT = get_open_trade_count()

    if (RISK_PERCENTAGE >= 0.5) and (OPEN_TRADE_COUNT >= 1):
        pass
    else:
        # The orderspecs
        mktOrder = MarketOrderRequest(
            instrument = instrument,
            units = UNIT_AMOUNT,
            takeProfitOnFill=TakeProfitDetails(price=TAKE_PROFIT_PRICE).data,
            # stopLossOnFill=StopLossDetails(price=STOP_LOSS).data,
            trailingStopLossOnFill=TrailingStopLossDetails(distance=TRAILING_STOP_DISTANCE).data
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

# get_instruments()
# print(risk_management('EUR_USD', 0.1, 2, 1, 1, 'SELL'))
# print(get_current_price('EUR_USD'))
# print(get_current_price('GBP_USD'))
# create_order('EUR_USD', 0.1, 'BUY')
