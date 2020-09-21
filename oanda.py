from oandapyV20 import API
from pandas import DataFrame
from decimal import Decimal
from oandapyV20.contrib.requests import (
    MarketOrderRequest,
    TakeProfitDetails,
    StopLossDetails,
    TrailingStopLossOrderRequest,
    TrailingStopLossDetails,
    TradeCloseRequest,
)

import oandapyV20
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing
import json
import requests
import time


class Oanda:


    def __init__(self, accountID, instrument, one_pip, risk_percentage, realorfake):
        self.accountID = accountID
        self.instrument = instrument
        self.one_pip = one_pip
        self.risk_percentage = risk_percentage
        self.realorfake = realorfake

        # print(token)

        if self.realorfake == 'REAL':
            # account authenticator returing access_token - real account
            self.token = "e84d432149ffdfa8ced7d52b864d7983-154be793312cd00759bef280e66b57c0"
            # api access key
            self.client = oandapyV20.API(access_token=(self.token), environment="live")
            self.api = oandapyV20.API(access_token=(self.token), environment="live")

        elif self.realorfake == 'FAKE':
            # account authenticator returing access_token - practise account
            self.token = "ace07448fdbcddf1d24c76db4f654abd-0673bb236877d296d74b63fef2d9be08"
            # api access key
            self.client = oandapyV20.API(access_token=(self.token))
            self.api = oandapyV20.API(access_token=(self.token))


    # # api access key
    # client = oandapyV20.API(access_token=token)
    # api = oandapyV20.API(access_token=token)


    def account(self):
        # requesting data
        r = accounts.AccountSummary(self.accountID)
        self.client.request(r)
        # saving the response into a dataframe
        response = DataFrame.from_dict(r.response)
        return response

    def trades(self):
        # requesting data
        r = trades.OpenTrades(self.accountID)
        self.client.request(r)
        # saving the response into a dataframe
        response = DataFrame.from_dict(r.response).iloc[0, 0]

        return response


        # ==============================================================================
        # returns account balance
    def get_balance(self):
        response = self.account()
        return (response.loc['balance', 'account'])

    # returns total profit loss on account
    def get_pl(self):
        response = self.account()
        return (response.loc['pl', 'account'])

    # returns id of most current open trade
    def get_open_trade(self):
        try:
            response = self.trades()
            id = response['id']

            if int(response['initialUnits']) > 0:
                direction = 'LONG'
            else:
                direction = 'SHORT'
            return id, direction
        except IndexError:
            return 0, 0

    # returns margin avaible
    def get_margin_available(self):
        response = self.account()
        return (response.loc['marginAvailable', 'account'])

    # returns margin used
    def get_margin_used(self):
        response = self.account()
        return (response.loc['marginUsed', 'account'])

    # returns total commission paid
    def get_commission(self):
        response = self.account()
        return (response.loc['commission', 'account'])

    # returns number of open trades
    def get_open_trade_count(self):
        response = self.account()
        return (response.loc['openTradeCount', 'account'])

    # returns current prices of trading instrument
    def get_current_price(self):
        # passing arguments
        params = {"instruments": self.instrument}
        # places request
        r = pricing.PricingInfo(accountID=self.accountID, params=params)
        rv = self.api.request(r)
        # BS ways of naigating json
        res = r.response['prices']
        df = DataFrame.from_dict(res, orient='columns')
        df = df.loc[0, 'closeoutBid']
        # returing the current price ask to 4 decimal places
        return float("{:.{}f}".format(float(df), 4))
    # ==============================================================================
    # returns list of instruments as output into instrument.txt, already ran once

    def get_instruments(self):
        # self.client = oandapyV20.API(access_token=token)

        r = accounts.AccountInstruments(accountID=self.accountID)
        rv = self.client.request(r)

        with open('instrument.txt', 'w') as outfile:
            json.dump(rv, outfile, indent=2)
    # ==============================================================================
    # CALULATIONS
    # calculates unit amount based of balance and risk percantge

    def unit_amount(self, buyorsell):
        current_price = self.get_current_price()
        leverage = 30
        balance = self.get_balance()
        risk_percentage = self.risk_percentage

        # unit_size = float(balance) * float(risk_percentage)
        unit_size = (float(balance) * float(leverage)) * float(risk_percentage)
        unit_amount = unit_size
        # unit_amount = float(unit_size) * float(current_price)

        if buyorsell == 'SELL':
            unit_amount = unit_amount * - 1
        elif buyorsell == 'BUY':
            unit_amount = unit_amount
        else:
            raise ValueError('Please enter BUY or SELL')

        return float((round(unit_amount)))

    # calculates the value of a single pip based of the unit amount
    def pip_value(self, buyorsell):
        CURRENT_PRICE = self.get_current_price()
        UNIT_AMOUNT = self.unit_amount(buyorsell)
        one_pip = float(self.one_pip)

        pip_value = (one_pip / CURRENT_PRICE) * UNIT_AMOUNT
        return round(pip_value, 2)

    # calculates take profit and stop loss based of balance available and risk percantge
    def risk_management(self, profit_ratio, loss_ratio, trailing_ratio, buyorsell):
        UNIT_AMOUNT = self.unit_amount(buyorsell)
        PIP_VALUE = self.pip_value(buyorsell)
        CURRENT_PRICE = self.get_current_price()
        pip = self.one_pip
        # getting the decimal place number e.g 0.0001 = 4th dp
        decimal_place = abs(Decimal(str(pip)).as_tuple().exponent)

        if buyorsell == 'BUY':
            if profit_ratio != 0:
                pip_gain = float(((self.risk_percentage * 100) / PIP_VALUE) * profit_ratio)
            else:
                pip_gain = float(((self.risk_percentage * 100) / PIP_VALUE) * 1)

            if loss_ratio != 0:
                pip_loss = (float(((self.risk_percentage * 100) / PIP_VALUE) * loss_ratio)) * -1
            else:
                pip_loss = (float(((self.risk_percentage * 100) / PIP_VALUE) * 1)) * -1

            if trailing_ratio != 0:
                pip_trailing = (float(((self.risk_percentage * 100) / PIP_VALUE) * trailing_ratio))
            else:
                pip_trailing = (float(((self.risk_percentage * 100) / PIP_VALUE) * 1))

        elif buyorsell == 'SELL':
            if profit_ratio != 0:
                pip_gain = float(((self.risk_percentage * 100) / PIP_VALUE) * profit_ratio)
            else:
                pip_gain = float(((self.risk_percentage * 100) / PIP_VALUE) * 1)

            if loss_ratio != 0:
                pip_loss = abs((float(((self.risk_percentage * 100) / PIP_VALUE) * loss_ratio)))
            else:
                pip_loss = abs((float(((self.risk_percentage * 100) / PIP_VALUE) * 1)))

            if trailing_ratio != 0:
                pip_trailing = abs((float(((self.risk_percentage * 100) / PIP_VALUE) * trailing_ratio)))
            else:
                pip_trailing = abs((float(((self.risk_percentage * 100) / PIP_VALUE) * 1)))

        take_profit = round((pip_gain * pip), decimal_place)
        stop_loss = round((pip_loss * pip), decimal_place)
        trailing_stop = round((pip_trailing * pip), decimal_place)

        take_profit_price = CURRENT_PRICE + take_profit
        stop_loss_price = CURRENT_PRICE + stop_loss
        # trailing stop is distnace therefore always positive
        trailing_stop_distance = trailing_stop
        # =======================================================================================================
        # temp soltion for The Trailing Stop Loss on fill price distance does not meet the minimum allowed amount
        # if trailing_stop_distance < 0.05:
        #     trailing_stop_distance = 0.05
        # =======================================================================================================
        print (take_profit_price, stop_loss_price, trailing_stop_distance, UNIT_AMOUNT)
        return take_profit_price, stop_loss_price, trailing_stop_distance

    # order template
    def create_order(self, order_type, buyorsell, tp=0.1, sl=0.05, ts=0.05):
        UNIT_AMOUNT = self.unit_amount(buyorsell)
        # sets take profit and trailing stop loss
        TAKE_PROFIT_PRICE, STOP_LOSS_PRICE, TRAILING_STOP_DISTANCE = self.risk_management(
            tp, sl, ts, buyorsell)
        RISK_PERCENTAGE = self.risk_percentage
        OPEN_TRADE_COUNT = self.get_open_trade_count()

        # if (RISK_PERCENTAGE >= 0.5) and (OPEN_TRADE_COUNT >= 1):
        #     pass
        # else:
        if order_type == 'ALL':
            # The orderspecs
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
                takeProfitOnFill=TakeProfitDetails(
                    price=TAKE_PROFIT_PRICE).data,
                stopLossOnFill=StopLossDetails(price=STOP_LOSS_PRICE).data,
                trailingStopLossOnFill=TrailingStopLossDetails(
                    distance=TRAILING_STOP_DISTANCE).data,
            )
        elif order_type == 'TPSL':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
                takeProfitOnFill=TakeProfitDetails(
                    price=TAKE_PROFIT_PRICE).data,
                stopLossOnFill=StopLossDetails(price=STOP_LOSS_PRICE).data,
            )
        elif order_type == 'TPTS':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
                takeProfitOnFill=TakeProfitDetails(
                    price=TAKE_PROFIT_PRICE).data,
                trailingStopLossOnFill=TrailingStopLossDetails(
                    distance=TRAILING_STOP_DISTANCE).data,
            )
        elif order_type == 'TS':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
                trailingStopLossOnFill=TrailingStopLossDetails(
                    distance=TRAILING_STOP_DISTANCE).data,
            )
        elif order_type == 'SL':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
                stopLossOnFill=StopLossDetails(price=STOP_LOSS_PRICE).data,
            )
        elif order_type == 'CROSS':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
            )
        elif order_type == 'NONE':
            mktOrder = MarketOrderRequest(
                instrument=self.instrument,
                units=UNIT_AMOUNT,
            )
        # print("Market Order specs: \n{}".format(json.dumps(mktOrder.data, indent=4)))
        # create the OrderCreate request
        r = orders.OrderCreate(self.accountID, data=mktOrder.data)
        try:
            # send the OrderCreate request
            rv = self.api.request(r)
        except oandapyV20.exceptions.V20Error as err:
            print(r.status_code, err)
        else:
            # print(json.dumps(rv, indent=2))
            try:
                data = DataFrame.from_dict(
                    rv['orderCancelTransaction'], orient='index')
                status = data.loc['type', 0]
                reason = data.loc['reason', 0]
                id = data.loc['id', 0]
                print('Order status:', status + '\n' +
                      'Reason:', reason + '\n' + 'Trade ID:', id)
            except KeyError:
                # KeyError to determin catch error raised by json return of 'orderCancelTransaction' instead of 'orderFillTransaction'
                data = DataFrame.from_dict(
                    rv['orderFillTransaction'], orient='index')
                status = data.loc['type', 0]
                id = data.loc['id', 0]
                print('Order status:', status + '\n' + 'Trade ID:', id)

                return id

    # close order
    def close_order(self, id):
        id = id
        ordr = TradeCloseRequest()
        r = trades.TradeClose(self.accountID, tradeID=id, data=ordr.data)
        # perform the request
        rv = self.client.request(r)
        data = DataFrame.from_dict(
            rv['orderCreateTransaction'], orient='index')
        trade_close = data.loc['tradeClose', 0]
        units_closed = trade_close['units']
        tradeID = trade_close['tradeID']
        print('Units closed:', units_closed + '\n' + 'Trade ID:', tradeID)

        return units_closed, tradeID

# account = '101-004-14591208-008'
# oa = Oanda(account, 'EUR_USD', 0.0001, 0.95, 'FAKE')
# print(oa.token)

# self.accountID = accountID
# self.instrument = instrument
# self.one_pip = one_pip
# self.risk_percentage = risk_percentage
# self.buyorsell = buyorsell
# sell = Oanda('101-004-14591208-002', 'EUR_USD', 0.0001, 1)
# print(sell.get_open_trade())
# sell.create_order('TS','BUY')
# id = 769
# time.sleep(15)
# sell.close_order(id)
