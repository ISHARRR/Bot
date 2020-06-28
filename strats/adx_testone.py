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


def adx_test_bot1(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    account = '101-004-14591208-007'

    oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')

    fast_ema = 270
    slow_ema = 630

    order_params = 'TS'

    while True:
        try:
            current_adx = adx.adx(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            email_message = 'ADX Crossover Strategy with TS'


            if bot.order_params(order_params):
                id, direction = oa.get_open_trade()
                # db.createDB(database, id, direction)

                buy_id = 0
                sell_id = 0

                if direction == 'LONG':
                    buy_id = id
                elif direction == 0:
                    buy_id

                if direction == 'SHORT':
                    sell_id = id
                elif direction == 0:
                    sell_id


            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx >=25)):  # BUY
                bot.trade_msg(stock_symbol, 'BUY')
                # email('BUY', stock_symbol, email_message)
                bot.email('BUY - Strong ADX', stock_symbol, email_message, 'private')

                if bot.order_params(order_params):
                    if sell_id != 0:
                        oa.close_order(sell_id)
                        print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                        bot.email('Order Closed', str(sell_id), 'Check if order has been closed', 'private')

                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, 'BUY', tp=0.1, sl=0, ts=0.1)

            elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx < 25 and current_adx > 10)):   # BUY
                bot.trade_msg(stock_symbol, 'BUY')
                # email('BUY', stock_symbol, email_message)
                bot.email('BUY - Weak ADX', stock_symbol, email_message, 'private')

                if bot.order_params(order_params):
                    if sell_id != 0:
                        oa.close_order(sell_id)
                        print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                        bot.email('Order Closed', str(sell_id), 'Check if order has been closed', 'private')

                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, 'BUY', tp=0.1, sl=0, ts=0.05)

            elif (adx < 10):
                break


                while True:
                    time.sleep(60)
                    try:
                        current_adx = adx.adx(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                            stock_symbol, api_key, fast_ema, slow_ema)


                        if bot.order_params(order_params):
                            id, direction = oa.get_open_trade()
                            # db.createDB(database, id, direction)

                            buy_id = 0
                            sell_id = 0

                            if direction == 'LONG':
                                buy_id = id
                            elif direction == 0:
                                buy_id

                            if direction == 'SHORT':
                                sell_id = id
                            elif direction == 0:
                                sell_id


                        if bot.order_params(order_params):
                            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)):  # SELL
                                if buy_id != 0:
                                    oa.close_order(buy_id)
                                    print('Trade ID:', buy_id,'Status: CLOSED' + '\n')
                                    bot.email('Order Closed - test', str(buy_id),'Check if order has been closed', 'private')


                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx >=25)):  # SELL
                            bot.trade_msg(stock_symbol, 'SELL')
                            # email('SELL', stock_symbol, email_message)
                            bot.email('SELL - Strong ADX', stock_symbol, email_message, 'private')

                            if oa.get_open_trade_count() < 1:
                                oa.create_order(order_params, 'SELL', tp=0.1, sl=0, ts=0.1)

                            break
                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx < 25 and current_adx > 10)):   # sell
                            bot.trade_msg(stock_symbol, 'SELL')
                            # email('SELL', stock_symbol, email_message)
                            bot.email('SELL - Weak ADX', stock_symbol, email_message, 'private')

                            if oa.get_open_trade_count() < 1:
                                oa.create_order(order_params, 'SELL', tp=0.1, sl=0, ts=0.05)

                            break

                        elif (adx < 10):
                            break

                    except Exception as e:
                        bot.exception_alert(e)
                        bot.email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(240)



            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx >=25)):  # SELL
                bot.trade_msg(stock_symbol, 'SELL')
                # email('SELL', stock_symbol, email_message)
                bot.email('SELL - Strong ADX', stock_symbol, email_message, 'private')

                if bot.order_params(order_params):
                    if buy_id != 0:
                        oa.close_order(buy_id)
                        print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                        bot.email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')

                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, 'SELL', tp=0.1, sl=0, ts=0.1)

            elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_adx < 25 and current_adx > 10)):  # SELL
                bot.trade_msg(stock_symbol, 'SELL')
                # email('SELL', stock_symbol, email_message)
                bot.email('SELL - Weak ADX', stock_symbol, email_message, 'private')

                if bot.order_params(order_params):
                    if buy_id != 0:
                        oa.close_order(buy_id)
                        print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                        bot.email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')

                if oa.get_open_trade_count() < 1:
                    oa.create_order(order_params, 'SELL', tp=0.1, sl=0, ts=0.05)

            elif (adx < 10):
                break



                while True:
                    time.sleep(60)
                    try:
                        current_adx = adx.adx(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                            stock_symbol, api_key, fast_ema, slow_ema)


                        if bot.order_params(order_params):
                            id, direction = oa.get_open_trade()
                            # db.createDB(database, id, direction)

                            buy_id = 0
                            sell_id = 0

                            if direction == 'LONG':
                                buy_id = id
                            elif direction == 0:
                                buy_id

                            if direction == 'SHORT':
                                sell_id = id
                            elif direction == 0:
                                sell_id


                        if bot.order_params(order_params):
                            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                                if sell_id != 0:
                                    oa.close_order(sell_id)
                                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                                    bot.email('Order Closed', str(sell_id),'Check if order has been closed', 'private')


                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx >=25)):  # BUY
                            bot.trade_msg(stock_symbol, 'BUY')
                            # email('BUY', stock_symbol, email_message)
                            bot.email('BUY - Stong ADX', stock_symbol, email_message, 'private')

                            if oa.get_open_trade_count() < 1:
                                oa.create_order(order_params, 'BUY', tp=0.1, sl=0, ts=0.1)

                            break

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_adx < 25 and current_adx > 10)):   # break
                            bot.trade_msg(stock_symbol, 'BUY')
                            # email('BUY', stock_symbol, email_message)
                            bot.email('BUY - Weak ADX', stock_symbol, email_message, 'private')

                            if oa.get_open_trade_count() < 1:
                                oa.create_order(order_params, 'BUY', tp=0.1, sl=0, ts=0.05)

                            break

                        elif (adx < 10):
                            break

                    except Exception as e:
                        bot.exception_alert(e)
                        bot.email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP',
                                  (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(240)

        except Exception as e:
            bot.exception_alert(e)
            bot.email('TEST BOT: EXCEPTION', 'ERROR',
                      (str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(60, 150))

        time.sleep(300)
