from indicators import (
    ema_sma,
    adx,

)
from trades_database import db
from datetime import datetime, time as t


import bot
import oanda
import time
import random
import traceback
import operator


def get_ids(order_params, oa):
    if bot.order_params(order_params):
        id, direction = oa.get_open_trade()
        buy_id, sell_id = bot.trade_ids(id, direction)
        return buy_id, sell_id


def inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, buyorsell, current_operator, previous_operator):
    while True:
        time.sleep(60)
        current_time = datetime.now().time()
        days = datetime.today().weekday()

        try:
            # current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            if bot.order_params(order_params):
                if ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow))):  # SELL
                    id, direction = oa.get_open_trade()
                    buy_id, sell_id = bot.trade_ids(id, direction)
                    if buyorsell == 'BUY':
                        if sell_id != 0:
                            oa.close_order(sell_id)
                            print('Trade ID:', sell_id,'Status: CLOSED' + '\n')
                            bot.email('Order Closed - test inner', str(sell_id),'Check if order has been closed', 'private')
                    elif buyorsell == 'SELL':
                        if buy_id != 0:
                            oa.close_order(buy_id)
                            print('Trade ID:', buy_id,'Status: CLOSED' + '\n')
                            bot.email('Order Closed - test inner', str(buy_id),'Check if order has been closed', 'private')


            # if ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow)) and (current_adx >= 25)):  # SELL
            if ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow))):
                bot.trade_msg(stock_symbol, buyorsell)
                bot.email(buyorsell + ' -', stock_symbol, email_message)
                if current_time >= t(00,00) and current_time <= t(12,00) and days == 0 and days ==1:
                    if oa.get_open_trade_count() < 1:
                        oa.create_order(order_params, buyorsell, tp=0.1, sl=0, ts=0.1)

                break

            # elif ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow)) and (current_adx < 25)):  # sell
            #
            #     break


        except Exception as e:
            bot.exception(e)

        time.sleep(inner_sleep)


def open_order(stock_symbol, order_params, oa, email_message, buyorsell, buyorsell_id):
    current_time = datetime.now().time()
    days = datetime.today().weekday()

    bot.trade_msg(stock_symbol, buyorsell)
    if bot.order_params(order_params):
        if buyorsell_id != 0:
            oa.close_order(buyorsell_id)
            print('Trade ID:', buyorsell_id, 'Status: CLOSED' + '\n')
            bot.email('Order Closed', str(buyorsell_id), 'Check if order has been closed', 'private')

    bot.email(buyorsell + ' -', stock_symbol, email_message)
    if current_time >= t(00,00) and current_time <= t(12,00) and days == 0 and days ==1:
        if oa.get_open_trade_count() < 1:
            oa.create_order(order_params, buyorsell, tp=0.1, sl=0, ts=0.05)


def adx_ema_sl_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    # real account
    account = '001-004-4069941-004'
    # practise account
    # account = '101-004-14591208-008'

    oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'REAL')
    # oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')

    fast_ema = 21
    slow_ema = 55

    outer_sleep = 300
    inner_sleep = 240

    order_params = 'CROSS'


    while True:
        try:
            # current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            email_message = 'EMA Crossover Strategy with ADX'


            # if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx >=25)): # BUY
            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)): # BUY
                buy_id, sell_id = get_ids(order_params, oa)
                open_order(stock_symbol, order_params, oa, email_message, 'BUY', sell_id)
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'SELL', operator.lt, operator.ge)

            # elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx >=25)):  # SELL
            elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)):  # SELL
                buy_id, sell_id = get_ids(order_params, oa)
                open_order(stock_symbol, order_params, oa, email_message, 'SELL', buy_id)
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'BUY', operator.gt, operator.le)


        except Exception as e:
            bot.exception(e)

        time.sleep(outer_sleep)
