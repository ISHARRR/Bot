from datetime import datetime
from indicators import (
    ema_sma,
    macd_strat,
)
from email.message import EmailMessage

from datetime import date

import time
import pytz
import random
import recipients
import oanda
import smtplib
import traceback
import os


def timezone(zone):
    z = pytz.timezone(zone)
    dt = datetime.now(z).strftime("%Y-%m-%d %H:%M:%S")

    return dt


def email(buyorsell, stock_symbol, context, privacy='public'):
    msg = EmailMessage()
    msg['Subject'] = buyorsell + ': ' + stock_symbol
    msg['From'] = 'isharreehal8@gmail.com'
    if privacy == 'public':
        msg['To'] = ", ".join(recipients.recipients())
    elif privacy == 'private':
        msg['To'] = ", ".join(recipients.recipients_test())
    msg.set_content(context)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

        smtp.send_message(msg)


def trading_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    tpsp = oanda.Oanda('101-004-14591208-002', oanda_stock_symbol, one_pip, 1)
    ts = oanda.Oanda('101-004-14591208-003', oanda_stock_symbol, one_pip, 1)
    tpts = oanda.Oanda('101-004-14591208-004', oanda_stock_symbol, one_pip, 1)
    all = oanda.Oanda('101-004-14591208-005', oanda_stock_symbol, one_pip, 1)

    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

            email_message = 'EMA Crossover Strategy - 30 min timeframe'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY
                print('BUY:', stock_symbol, time_msg)
                email('BUY', stock_symbol, email_message)

                tpsp.create_order('TPSP', 'BUY')
                ts.create_order('TS', 'BUY')
                tpts.create_order('TPTS', 'BUY')
                all.create_order('ALL', 'BUY')

                time.sleep(1260)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                print('SELL:', stock_symbol, time_msg)
                email('SELL', stock_symbol, email_message)

                tpsp.create_order('TPSP', 'SELL')
                ts.create_order('TS', 'SELL')
                tpts.create_order('TPTS', 'SELL')
                all.create_order('ALL', 'SELL')

                time.sleep(1260)

        except Exception as e:
            window_len = os.popen('stty size', 'r').read().split()
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e) + '\n')
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            time.sleep(random.randint(30, 150))
            email('MAIN BOT - EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')

        time.sleep(600)


def trading_bot_test(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    cross = oanda.Oanda('101-004-14591208-007', oanda_stock_symbol, one_pip, 1)

    buy_id = 0
    sell_id = 0
    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

            email_message = 'Crossover Strategy'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY
                print('BUY:', stock_symbol, time_msg)
                # email('BUY', stock_symbol, email_message)
                email('BUY - test', stock_symbol, email_message, 'private')
                if sell_id != 0:
                    cross.close_order(sell_id)
                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                    sell_id = 0
                buy_id = cross.create_order('CROSS', 'BUY')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)): # SELL
                            if buy_id != 0:
                                cross.close_order(buy_id)
                                print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                                buy_id = 0
                        # if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                            print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                            print('SELL:', stock_symbol, time_msg)
                            # email('SELL', stock_symbol, email_message)
                            email('SELL - test', stock_symbol, email_message, 'private')
                            sell_id = cross.create_order('CROSS', 'SELL')
                            break
                        # elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow < current_sma200)): # breakout
                        #     break

                    except Exception as e :
                        window_len = os.popen('stty size', 'r').read().split()
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(30, 150))

                    time.sleep(540)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                print('SELL:', stock_symbol, time_msg)
                # email('SELL', stock_symbol, email_message)
                email('SELL - test', stock_symbol, email_message, 'private')
                if buy_id != 0:
                    cross.close_order(buy_id)
                    print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                    buy_id = 0
                sell_id = cross.create_order('CROSS', 'SELL')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                            if sell_id != 0:
                                cross.close_order(sell_id)
                                print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                                sell_id = 0
                        # if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)):  # BUY
                            print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                            print('BUY:', stock_symbol, time_msg)
                            # email('BUY', stock_symbol, email_message)
                            email('BUY - test', stock_symbol, email_message, 'private')
                            buy_id = cross.create_order('CROSS', 'BUY')
                            break
                        # elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow > current_sma200)): # breakout
                        #     break

                    except Exception as e :
                        window_len = os.popen('stty size', 'r').read().split()
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(30, 150))

                    time.sleep(540)

        except Exception as e :
            window_len = os.popen('stty size', 'r').read().split()
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(30, 150))

        time.sleep(600)


def trading_bot_test1(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    cross = oanda.Oanda('101-004-14591208-007', oanda_stock_symbol, one_pip, 1)

    buy_id = 0
    sell_id = 0
    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

            email_message = 'Crossover Strategy'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY
                print('BUY:', stock_symbol, time_msg)
                # email('BUY', stock_symbol, email_message)
                email('BUY - test', stock_symbol, email_message, 'private')
                if sell_id != 0:
                    cross.close_order(sell_id)
                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                    sell_id = 0
                buy_id = cross.create_order('CROSS', 'BUY')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)): # SELL
                            if buy_id != 0:
                                cross.close_order(buy_id)
                                print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                                buy_id = 0
                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                            print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                            print('SELL:', stock_symbol, time_msg)
                            # email('SELL', stock_symbol, email_message)
                            email('SELL - test', stock_symbol, email_message, 'private')
                            sell_id = cross.create_order('CROSS', 'SELL')
                            break
                        elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow < current_sma200)): # breakout
                            break

                    except Exception as e :
                        window_len = os.popen('stty size', 'r').read().split()
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(30, 150))

                    time.sleep(540)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                print('SELL:', stock_symbol, time_msg)
                # email('SELL', stock_symbol, email_message)
                email('SELL - test', stock_symbol, email_message, 'private')
                if buy_id != 0:
                    cross.close_order(buy_id)
                    print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                    buy_id = 0
                sell_id = cross.create_order('CROSS', 'SELL')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                            if sell_id != 0:
                                cross.close_order(sell_id)
                                print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                                sell_id = 0
                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)):  # BUY
                            print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                            print('BUY:', stock_symbol, time_msg)
                            # email('BUY', stock_symbol, email_message)
                            email('BUY - test', stock_symbol, email_message, 'private')
                            buy_id = cross.create_order('CROSS', 'BUY')
                            break
                        elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow > current_sma200)): # breakout
                            break

                    except Exception as e :
                        window_len = os.popen('stty size', 'r').read().split()
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
                        print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(30, 150))

                    time.sleep(540)

        except Exception as e :
            window_len = os.popen('stty size', 'r').read().split()
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e))
            print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
            email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(30, 150))

        time.sleep(600)


def trading_bot_test2(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    if date.today().weekday() == 0:

        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')
        time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
        print(stock_symbol, 'Running...', time_msg )

        tpsp = oanda.Oanda('101-004-14591208-002', oanda_stock_symbol, one_pip, 1)
        ts = oanda.Oanda('101-004-14591208-003', oanda_stock_symbol, one_pip, 1)
        tpts = oanda.Oanda('101-004-14591208-004', oanda_stock_symbol, one_pip, 1)
        all = oanda.Oanda('101-004-14591208-005', oanda_stock_symbol, one_pip, 1)

        while True:
            ny_time = timezone('America/New_york')
            uk_time = timezone('Europe/London')

            time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

            try:
                current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                email_message = 'EMA Crossover Strategy - 30 min timeframe'

                if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY
                    print('BUY:', stock_symbol, time_msg)
                    email('BUY', stock_symbol, email_message)

                    tpsp.create_order('TPSP', 'BUY')
                    ts.create_order('TS', 'BUY')
                    tpts.create_order('TPTS', 'BUY')
                    all.create_order('ALL', 'BUY')

                    time.sleep(1260)

                if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                    print('SELL:', stock_symbol, time_msg)
                    email('SELL', stock_symbol, email_message)

                    tpsp.create_order('TPSP', 'SELL')
                    ts.create_order('TS', 'SELL')
                    tpts.create_order('TPTS', 'SELL')
                    all.create_order('ALL', 'SELL')

                    time.sleep(1260)

            except Exception as e:
                window_len = os.popen('stty size', 'r').read().split()
                print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e) + '\n')
                print (' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
                time.sleep(random.randint(30, 150))
                email('MAIN BOT - EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')

            time.sleep(600)
