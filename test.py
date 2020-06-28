
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


def adx_test_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    account = '101-004-14591208-008'

    oa = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')
    # database = 'trades_database/adx_testDB'
    oa.create_order('CROSS', 'BUY', tp=0, sl=0.1, ts=0)

adx_test_bot('EURUSD', 0.0001, 'AGB2JDHJFGRI89VB', 'EUR_USD')





# from alpha_vantage.techindicators import TechIndicators
# import oanda
#
#
#
# def order_params(param):
#     if param == 'CROSS':
#         return True
#     elif param == 'SL':
#         return True
#     else:
#         return False
#
# print(order_params('sl'))
#
#
#
# # oa = oanda.Oanda('101-004-14591208-002', 'EUR_USD', 0.0001, 0.95)
# #
# #
# # id, diect = oa.get_open_trade()
# #
# # print(id, diect)
#
# def ema(stock_symbol, api_key, period):
#     # variable for indicator
#     ti = TechIndicators(key=api_key, output_format='pandas')
#     # ema tim period eg 5 = 150 on 30 mins time frame
#     period = period
#
#     try:
#     # ema
#         if period > 1000:
#             print('call1')
#             data_ema, meta_data_ema = ti.get_ema(
#                 symbol=stock_symbol,
#                 series_type='close',
#                 interval='5min',
#                 time_period=(int(period/5)),
#                 )
#             # getting the second most current value aka the n-1
#             previous_ema = data_ema['EMA'].iloc[-7]
#
#         else:
#             print('call2')
#             data_ema, meta_data_ema = ti.get_ema(
#                 symbol=stock_symbol,
#                 series_type='close',
#                 interval='1min',
#                 time_period=period,
#                 )
#             # getting the second most current value aka the n-1
#             previous_ema = data_ema['EMA'].iloc[-1000]
#
#         # getting the most current value aka the n (tail)current_ema
#         current_ema = data_ema['EMA'].iloc[-1]
#     except:
#         pass
#     else:
#         if period > 400:
#             print('call3')
#             data_ema, meta_data_ema = ti.get_ema(
#                 symbol=stock_symbol,
#                 series_type='close',
#                 interval='5min',
#                 time_period=(int(period/5)),
#                 )
#             # getting the second most current value aka the n-1
#             previous_ema = data_ema['EMA'].iloc[-7]
#
#         else:
#             print('call4')
#             data_ema, meta_data_ema = ti.get_ema(
#                 symbol=stock_symbol,
#                 series_type='close',
#                 interval='1min',
#                 time_period=period,
#                 )
#             # getting the second most current value aka the n-1
#             previous_ema = data_ema['EMA'].iloc[-31]
#
#         # getting the most current value aka the n (tail)current_ema
#         current_ema = data_ema['EMA'].iloc[-1]
#
#
#     return current_ema, previous_ema
#
# # print(ema('EURUSD', '4HKNDHHTQH2CFWZ9', 800))
