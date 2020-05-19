from datetime import datetime
from indicators import (
    ema_sma,
    macd_strat,
)
from email.message import EmailMessage

import time
import pytz
import random
import recipients
import oanda
import smtplib


def timezone(zone):
    z = pytz.timezone(zone)
    dt = datetime.now(z).strftime("%Y-%m-%d %H:%M:%S")

    return dt


def email(buyorsell, stock_symbol, strategy):
    msg = EmailMessage()
    msg['Subject'] = buyorsell + ': ' + stock_symbol
    msg['From'] = 'isharreehal8@gmail.com'
    msg['To'] = ", ".join(recipients.recipients())
    # msg['To'] = ", ".join(recipients.recipients_test())
    msg.set_content(strategy)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

        smtp.send_message(msg)


def ema(stock_symbol, one_pip, api_key, oanda_stock_symbol):
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

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast < previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY
                print('BUY:', stock_symbol, time_msg)
                email('BUY', stock_symbol, email_message)

                tpsp.create_order('TPSP', 'BUY')
                ts.create_order('TS', 'BUY')
                tpts.create_order('TPTS', 'BUY')
                all.create_order('ALL', 'BUY')

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast > previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                print('SELL:', stock_symbol, time_msg)
                email('SELL', stock_symbol, email_message)

                tpsp.create_order('TPSP', 'SELL')
                ts.create_order('TS', 'SELL')
                tpts.create_order('TPTS', 'SELL')
                all.create_order('ALL', 'SELL')

        except Exception as e :
            print ('EXCEPTION ERROR', time_msg + '\n' + str(e))
            time.sleep(random.randint(30, 150))

        time.sleep(600)
