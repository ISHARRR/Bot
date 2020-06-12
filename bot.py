from datetime import datetime
from email.message import EmailMessage
from strats import (
    crossover,
    sma_crossover,
    basic,
    adx_ema,
)


from datetime import date


import pytz
import recipients
import smtplib
import os
import traceback


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


def exception_alert(e):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time + ') ' + \
        '| UK-Time:' + '(' + uk_time + ')'
    window_len = os.popen('stty size', 'r').read().split()
    print(' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
    print('EXCEPTION ERROR', time_msg + '\n' + str(e) + '\n')
    # print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e) + '\n')
    print(' EXCEPTION ERROR '.center(int(window_len[1]), '*') + '\n')


def running_msg(stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time + ') ' + \
        '| UK-Time:' + '(' + uk_time + ')'
    print(stock_symbol, 'Running...', time_msg)


def trade_msg(stock_symbol, buyorsell):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = '- ' + 'NY-Time:' + \
        '(' + ny_time + ') ' + '| UK-Time:' + '(' + uk_time + ')'
    print(buyorsell + ':', stock_symbol, time_msg)


# active bots


def basic_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    basic.basic_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    crossover.crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def sma_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    sma_crossover.sma_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def adx_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    adx_ema.adx_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)
