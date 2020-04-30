from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from email.message import EmailMessage
from threading import Thread

import matplotlib
import os
import time
import smtplib
import pytz
import random
import recipients


def timezone(zone):
    z = pytz.timezone(zone)
    dt = datetime.now(z).strftime("%Y-%m-%d %H:%M:%S")

    return dt


def email(buyorsell, stock_symbol):
    msg = EmailMessage()
    msg['Subject'] = buyorsell + ': ' + stock_symbol
    msg['From'] = 'isharreehal8@gmail.com'
    msg['To'] = ", ".join(recipients.recipients())
    # msg['To'] = ", ".join(recipients.recipients_test())
    msg.set_content('CHECK OVERALL TREND')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

        smtp.send_message(msg)


def ema(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')
    # ema
    data_ema5, meta_data_ema = ti.get_ema(symbol = stock_symbol, series_type = 'close', interval='1min', time_period=150)
    data_ema15, meta_data_ema = ti.get_ema(symbol= stock_symbol, series_type = 'close', interval='1min', time_period=450)

    #print (data_ema5.iloc[-31:-1], '\n')
    #print (data_ema15.iloc[-31:-1], '\n')

    # getting the most current value aka the n (tail)
    current_ema5 = data_ema5['EMA'].iloc[-1]
    current_ema15 = data_ema15['EMA'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_ema5 = data_ema5['EMA'].iloc[-31]
    previous_ema15 = data_ema15['EMA'].iloc[-31]

    return current_ema5, current_ema15, previous_ema5, previous_ema15


def sma(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')
    # sma
    data_sma100, meta_data_ema = ti.get_sma(symbol = stock_symbol, series_type = 'close', interval='1min', time_period=3000)
    data_sma200, meta_data_ema = ti.get_sma(symbol= stock_symbol, series_type = 'close', interval='1min', time_period=6000)
    # getting the most current value aka the n (tail)
    current_sma100 = data_sma100['SMA'].iloc[-1]
    current_sma200 = data_sma200['SMA'].iloc[-1]

    return current_sma100, current_sma200


def trade(stock_symbol, api_key):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_sma100, current_sma200 = sma(stock_symbol, api_key)
            current_ema5, current_ema15, previous_ema5, previous_ema15 = ema(stock_symbol, api_key)

            if ( (current_ema5 < current_ema15) and (previous_ema5 > previous_ema15) and (current_sma100 > current_sma200) ): # BUY
                print('BUY:', stock_symbol, time_msg)
                email('BUY', stock_symbol)
                time.sleep(1200)

            if ( (current_ema5 > current_ema15) and (previous_ema5 < previous_ema15) and (current_sma100 < current_sma200) ): # SELL
                print('SELL:', stock_symbol, time_msg)
                email('SELL', stock_symbol)
                time.sleep(1200)

        except:
            print ('EXCEPTION ERROR', time_msg)
            time.sleep(random.randint(30, 150))

        time.sleep(300)

# ema('USDEUR', '4OKNDHHTQH2CFWZ9')
# ema('USDGBP', 'T7NT8GKR7CJ36U3C')
