from alpha_vantage.techindicators import TechIndicators


def ema(stock_symbol, api_key, period):
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # ema tim period eg 5 = 150 on 30 mins time frame
    period = period

    # ema
    if period > 1000:
        data_ema, meta_data_ema = ti.get_ema(
            symbol=stock_symbol,
            interval='5min',
            time_period=(int(period/5)),
            )
        # getting the second most current value aka the n-1
        previous_ema = data_ema['EMA'].iloc[-14]

    else:
        data_ema, meta_data_ema = ti.get_ema(
            symbol=stock_symbol,
            interval='1min',
            time_period=period,
            )
        # getting the second most current value aka the n-1
        previous_ema = data_ema['EMA'].iloc[-61]

    # getting the most current value aka the n (tail)current_ema
    current_ema = data_ema['EMA'].iloc[-1]

    return current_ema, previous_ema


def double_ema(stock_symbol, api_key, fast, slow):
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # 10 day ema
    fast_period = fast
    # 30 day ema
    slow_period = slow
    # ema

    data_ema_fast, meta_data_ema = ti.get_ema(
        symbol=stock_symbol,
        interval='30min',
        time_period=fast_period
        )

    data_ema_slow, meta_data_ema = ti.get_ema(
        symbol=stock_symbol,
        interval='30min',
        time_period=(slow_period)
        )

    # getting the most current value aka the n (tail)
    current_ema_fast = data_ema_fast['EMA'].iloc[-1]
    current_ema_slow = data_ema_slow['EMA'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_ema_slow = data_ema_slow['EMA'].iloc[-3]
    previous_ema_fast = data_ema_fast['EMA'].iloc[-3]

    return current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow



# def double_ema(stock_symbol, api_key, fast, slow):
#     # variable for indicator
#     ti = TechIndicators(key=api_key, output_format='pandas')
#     # 10 day ema
#     fast_period = fast
#     # 30 day ema
#     slow_period = slow
#     # ema
#     if fast > 1000:
#         data_ema_fast, meta_data_ema = ti.get_ema(
#             symbol=stock_symbol,
#             series_type='close',
#             interval='5min',
#             time_period=(int(slow_period/5))
#             )
#         previous_ema_fast = data_ema_fast['EMA'].iloc[-14]
#     else:
#         data_ema_fast, meta_data_ema = ti.get_ema(
#             symbol=stock_symbol,
#             series_type='close',
#             interval='1min',
#             time_period=fast_period
#             )
#         previous_ema_fast = data_ema_fast['EMA'].iloc[-61]
#
#     if slow > 1000:
#         data_ema_slow, meta_data_ema = ti.get_ema(
#             symbol=stock_symbol,
#             series_type='close',
#             interval='5min',
#             time_period=(int(slow_period/5))
#             )
#         # getting the second most current value aka the n-1
#         previous_ema_slow = data_ema_slow['EMA'].iloc[-14]
#
#     else:
#         data_ema_slow, meta_data_ema = ti.get_ema(
#             symbol=stock_symbol,
#             series_type='close',
#             interval='1min',
#             time_period=(slow_period)
#             )
#         # getting the second most current value aka the n-1
#         previous_ema_slow = data_ema_slow['EMA'].iloc[-61]
#
#     # print (data_ema_fast.iloc[-31:-1], '\n')
#     # print (data_ema_slow.iloc[-31:-1], '\n')
#
#     # getting the most current value aka the n (tail)
#     current_ema_fast = data_ema_fast['EMA'].iloc[-1]
#     current_ema_slow = data_ema_slow['EMA'].iloc[-1]
#
#     return current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow


def sma(stock_symbol, api_key, period=200):
    # 100 day period sma = 600 and 200 = 1200
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # sma
    data_sma, meta_data_sma = ti.get_sma(
        symbol=stock_symbol,
        interval='30min',
        time_period=period)
    # getting the most current value aka the n (tail)
    current_sma = data_sma['SMA'].iloc[-1]
    # return current_sma200
    return current_sma

# print(sma('EURUSD', '4OKNDHHTQH2CFWZ9', 200))
