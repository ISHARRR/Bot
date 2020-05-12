from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


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
    data_sma100, meta_data_sma = ti.get_sma(symbol = stock_symbol, series_type = 'close', interval='5min', time_period=600)
    data_sma200, meta_data_sma = ti.get_sma(symbol= stock_symbol, series_type = 'close', interval='5min', time_period=1200)
    # getting the most current value aka the n (tail)
    current_sma100 = data_sma100['SMA'].iloc[-1]
    current_sma200 = data_sma200['SMA'].iloc[-1]
    # return current_sma200
    return current_sma100, current_sma200
