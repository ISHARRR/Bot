from indicators import (
    ema_sma,

)

import bot
import oanda
import time
import random
import traceback


def basic_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    ts = oanda.Oanda('101-004-14591208-003', oanda_stock_symbol, one_pip, 0.95)
    tpts = oanda.Oanda('101-004-14591208-004', oanda_stock_symbol, one_pip, 0.95)

    while True:
        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(
                stock_symbol, api_key)

            email_message = 'EMA Crossover Strategy - 30 min timeframe'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow > current_sma200)):  # BUY
                bot.trade_msg(stock_symbol, 'BUY')
                bot.email('BUY', stock_symbol, email_message)

                ts.create_order('TS', 'BUY')
                tpts.create_order('TPTS', 'BUY')

                time.sleep(1560)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow < current_sma200)):  # SELL
                bot.trade_msg(stock_symbol, 'SELL')
                bot.email('SELL', stock_symbol, email_message)

                ts.create_order('TS', 'SELL')
                tpts.create_order('TPTS', 'SELL')

                time.sleep(1560)

        except Exception as e:
            bot.exception_alert(e)
            time.sleep(random.randint(60, 150))
            bot.email('MAIN BOT - EXCEPTION', 'ERROR',
                      (str(traceback.format_exc()) + '\n' + str(e)), 'private')

        time.sleep(300)
