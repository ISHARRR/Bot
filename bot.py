from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from email.message import EmailMessage
from threading import Thread

import matplotlib
import matplotlib.pyplot as plt
import os
import time
import smtplib
import pytz
import random

def timezone():
    ny_timezone = pytz.timezone('America/New_york')
    datetime_NY = datetime.now(ny_timezone).strftime("%H:%M:%S")
    
    uk_timezone = pytz.timezone('Europe/London')
    datetime_UK = datetime.now(uk_timezone).strftime("%H:%M:%S")
    
    return datetime_NY, datetime_UK

def email(buyorsell, stock_symbol):
    recipients = ['isharreehal8@gmail.com',
                  'rehmatk08@gmail.com',
                 ]

    msg = EmailMessage()
    msg['Subject'] = buyorsell + ': ' + stock_symbol
    msg['From'] = 'isharreehal8@gmail.com'
    msg['To'] = ", ".join(recipients)
    msg.set_content('CHECK OVERALL TREND')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

        smtp.send_message(msg)


def ema(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')

    data_ema5, meta_data_ema = ti.get_ema(symbol = stock_symbol, interval='1min', time_period=450)
    data_ema15, meta_data_ema = ti.get_ema(symbol= stock_symbol, interval='1min', time_period=150)

    # getting the most current value aka the n (tail)
    current_ema5 = data_ema5['EMA'].iloc[-1]
    current_ema15 = data_ema15['EMA'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_ema5 = data_ema5['EMA'].iloc[-15]
    previous_ema15 = data_ema15['EMA'].iloc[-15]

    return current_ema5, current_ema15, previous_ema5, previous_ema15

def trade(stock_symbol, api_key):
    print(stock_symbol, 'Running...')
    
    while True:
        ny_time, uk_time = timezone()
        
        try:
            current_ema5, current_ema15, previous_ema5, previous_ema15 = ema(stock_symbol, api_key)
        
        #print (stock_symbol, ': ','5 =', current_ema5, '15 =', current_ema15, 'p5 =', previous_ema5, 'p15 =', previous_ema15,
        #        '\n','NY Time :', ny_time, '\n', 'UK Time :', uk_time)

            if (current_ema5 > current_ema15) and (previous_ema5 < previous_ema15): # BUY
                print('BUY:', stock_symbol, '  - NY Time :', ny_time, '  - UK Time :', uk_time)
                email('BUY', stock_symbol)

            if (current_ema5 < current_ema15) and (previous_ema5 > previous_ema15): # SELL
                print('SELL:', stock_symbol, '  - NY Time :', ny_time, '  - UK Time :', uk_time)
                email('SELL', stock_symbol)
        except:
            print ('EXCEPTION ERROR' + ' Time:', ny_time)
            time.sleep(random.randint(30, 150))
 
            

        time.sleep(300)
