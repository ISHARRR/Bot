from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


def adx(stock_symbol, api_key, interval='30min'):
    ti = TechIndicators(key=api_key, output_format='pandas')

    time_period=14

    data_adx, meta_data_adx = ti.get_adx(
        symbol=stock_symbol,
        interval=interval,
        time_period=time_period,

    )

    # longterm_adx = sum(data_adx['ADX'].iloc[-1440:])/1440
    current_adx = data_adx['ADX'].iloc[-1]

    return current_adx


def adx1(stock_symbol, api_key, interval='30min'):
    ti = TechIndicators(key=api_key, output_format='pandas')

    time_period=14

    data_adx, meta_data_adx = ti.get_adx(
        symbol=stock_symbol,
        interval=interval,
        time_period=time_period,

    )

    # longterm_adx = sum(data_adx['ADX'].iloc[-1440:])/1440
    current_adx = data_adx['ADX'].iloc[-1]
    previous_adx = data_adx['ADX'].iloc[-2]

    return current_adx, previous_adx


# print(adx('EURUSD', 'ARA2JDHJFGRI89VB'))
