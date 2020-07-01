from indicators import (
    ema_sma,
    adx,

)
from trades_database import db


import bot
import oanda
import time
import random
import traceback
import operator


def inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, buyorsell, current_operator, previous_operator):
    while True:
        time.sleep(60)
        try:
            current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            if bot.order_params(order_params):
                id, direction = oa.get_open_trade()
                buy_id, sell_id = bot.trade_ids(id, direction)
                if ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow))):  # SELL
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


            if ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow)) and (current_adx >= 25)):  # SELL
                bot.trade_msg(stock_symbol, buyorsell)
                bot.email(buyorsell + ' - Weak ADX inner', stock_symbol, email_message, 'private')
                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, buyorsell, tp=0, sl=0, ts=0.05)

                break

            elif ((current_operator(current_ema_fast, current_ema_slow)) and (previous_operator(previous_ema_fast, previous_ema_slow)) and (current_adx < 25)):  # sell
                bot.trade_msg(stock_symbol, buyorsell)
                bot.email(buyorsell + ' - Weak ADX inner', stock_symbol, email_message, 'private')
                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, buyorsell, tp=0, sl=0, ts=0.05)

                break


        except Exception as e:
            bot.exception(e)

        time.sleep(inner_sleep)


def open_order(stock_symbol, order_params, oa, email_message, buyorsell, buyorsell_id, strongorweak):
    bot.trade_msg(stock_symbol, buyorsell)
    if bot.order_params(order_params):
        if buyorsell_id != 0:
            oa.close_order(buyorsell_id)
            print('Trade ID:', buyorsell_id, 'Status: CLOSED' + '\n')
            bot.email('Order Closed', str(buyorsell_id), 'Check if order has been closed', 'private')

    if oa.get_open_trade_count() < 1:
        if strongorweak == 'STRONG':
            bot.email('SELL - Strong ADX', stock_symbol, email_message, 'private')
            oa.create_order(order_params, buyorsell, tp=0, sl=0, ts=0.1)
        elif strongorweak == 'WEAK':
            bot.email('SELL - Weak ADX', stock_symbol, email_message, 'private')
            oa.create_order(order_params, buyorsell, tp=0, sl=0, ts=0.05)



def adx_test_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    # account = '001-004-4069941-004'
    account = '101-004-14591208-008'

    # oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'REAL')
    oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')

    fast_ema = 9
    slow_ema = 21

    outer_sleep = 300
    inner_sleep = 240

    order_params = 'TS'


    while True:
        try:
            current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            email_message = 'ADX Crossover Strategy with TS'

            if bot.order_params(order_params):
                id, direction = oa.get_open_trade()
                buy_id, sell_id = bot.trade_ids(id, direction)

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx >=25)):  # BUY
                open_order(stock_symbol, order_params, oa, email_message, 'BUY', sell_id, 'STRONG')
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'SELL', operator.lt, operator.ge)

            elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx < 25)):  # BUY
                open_order(stock_symbol, order_params, oa, email_message, 'BUY', sell_id, 'WEAK')
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'SELL', operator.lt, operator.ge)

            elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx >=25)):  # SELL
                open_order(stock_symbol, order_params, oa, email_message, 'SELL', buy_id, 'STRONG')
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'BUY', operator.gt, operator.le)

            elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx < 25)):   # SELL
                open_order(stock_symbol, order_params, oa, email_message, 'SELL', buy_id, 'WEAK')
                # WhILE LOOP
                inner_loop(stock_symbol, api_key, inner_sleep, oa, fast_ema, slow_ema, order_params, email_message, 'BUY', operator.gt, operator.le)


        except Exception as e:
            bot.exception(e)

        time.sleep(outer_sleep)
