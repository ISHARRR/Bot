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

    order = oanda.Oanda('101-004-14591208-001', oanda_stock_symbol, one_pip, 1)

    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        # try:
        current_sma100, current_sma200 = ema_sma.sma(stock_symbol, api_key)
        current_ema5, current_ema15, previous_ema5, previous_ema15 = ema_sma.ema(stock_symbol, api_key)

        email_message = 'EMA Crossover Strategy - 30 min timeframe'

        if ((current_ema5 > current_ema15) and (previous_ema5 < previous_ema15) and (current_sma100 > current_sma200)): # BUY
            print('BUY:', stock_symbol, time_msg)
            email('BUY', stock_symbol, email_message)
            order.create_order('BUY')
            time.sleep(1100)

        if ((current_ema5 < current_ema15) and (previous_ema5 > previous_ema15) and (current_sma100 < current_sma200)): # SELL
            print('SELL:', stock_symbol, time_msg)
            email('SELL', stock_symbol, email_message)
            order.create_order('SELL')
            time.sleep(1100)

        # except:
        #     print ('EXCEPTION ERROR', time_msg)
        #     time.sleep(random.randint(30, 150))

        time.sleep(600)


def macd(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    order = oanda.Oanda('101-004-14591208-003', oanda_stock_symbol, one_pip, 1)

    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_macd, current_macd_signal, previous_macd, previous_macd_signal = macd_strat.macd(stock_symbol, api_key)

            email_message = 'MACD Strategy - 15 min timeframe'

            if ((current_macd > current_macd_signal) and (previous_macd < previous_macd_signal) and (current_macd < 0)): # BUY
                print('BUY:', stock_symbol, time_msg)
                email('BUY', stock_symbol, email_message)
                order.create_order('BUY')
                time.sleep(660)

            if ((current_macd < current_macd_signal) and (current_macd > current_macd_signal) and (current_macd > 0)): # SELL
                print('SELL:', stock_symbol, time_msg)
                email('SELL', stock_symbol, email_message)
                order.create_order('SELL')
                time.sleep(660)

        except:
            print ('EXCEPTION ERROR', time_msg)
            time.sleep(random.randint(30, 150))

        time.sleep(300)

# sma('EURUSD', '4OKNDHHTQH2CFWZ9')
# ema('GBPUSD', 'T7NT8GKR7CJ36U3C')
