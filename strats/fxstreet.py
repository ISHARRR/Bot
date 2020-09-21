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
    if current_time >= t(00,00) and current_time <= t(12,00) and days == 0 or days == 1:
        if oa.get_open_trade_count() < 1:
            oa.create_order(order_params, buyorsell, tp=0, sl=0, ts=0)


def fxstreet_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    # REAL ACCOUNT
    # account = '001-004-4069941-004'
    # oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'REAL')

    # PRACTISE ACCOUNT
    account = '101-004-14591208-008'
    oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')

    fast_ema = 21
    slow_ema = 55

    outer_sleep = 300
    inner_sleep = 240

    order_params = 'NONE'

    fxstreet = 'BUY'
    fxstreet = 'SELL'

    while True:
        try:
            # current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            email_message = 'EMA Crossover Strategy with FX Street'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)) and (fxstreet == 'BUY'): # BUY
                buy_id, sell_id = get_ids(order_params, oa)
                open_order(stock_symbol, order_params, oa, email_message, 'BUY', sell_id)

            elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)) and (fxstreet == 'SELL'):  # SELL
                buy_id, sell_id = get_ids(order_params, oa)
                open_order(stock_symbol, order_params, oa, email_message, 'SELL', buy_id)

        except Exception as e:
            bot.exception(e)

        time.sleep(outer_sleep)
