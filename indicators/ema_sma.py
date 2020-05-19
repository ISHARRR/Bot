from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


def ema_10_30(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')
    # 10 day ema
    fast_period = 300
    # 30 day ema
    slow_period = 900
    # ema
    data_ema_fast, meta_data_ema = ti.get_ema(symbol = stock_symbol, series_type = 'close', interval='1min', time_period=fast_period)
    data_ema_slow, meta_data_ema = ti.get_ema(symbol= stock_symbol, series_type = 'close', interval='1min', time_period=slow_period)

    # print (data_ema_fast.iloc[-31:-1], '\n')
    # print (data_ema_slow.iloc[-31:-1], '\n')

    # getting the most current value aka the n (tail)
    current_ema_fast = data_ema_fast['EMA'].iloc[-1]
    current_ema_slow = data_ema_slow['EMA'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_ema_fast = data_ema_fast['EMA'].iloc[-31]
    previous_ema_slow = data_ema_slow['EMA'].iloc[-31]

    return current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow


def sma_100(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')
    # 100 day sma
    period = 600
    # sma
    data_sma100, meta_data_sma = ti.get_sma(symbol = stock_symbol, series_type = 'close', interval='5min', time_period=period)
    # getting the most current value aka the n (tail)
    current_sma100 = data_sma100['SMA'].iloc[-1]
    # return current_sma200
    return current_sma100


def sma_200(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')
    # 200 day sma
    period = 1200
    # sma
    data_sma200, meta_data_sma = ti.get_sma(symbol= stock_symbol, series_type = 'close', interval='5min', time_period=period)
    # getting the most current value aka the n (tail)
    current_sma200 = data_sma200['SMA'].iloc[-1]
    # return current_sma200
    return current_sma200
