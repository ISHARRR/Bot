
from alpha_vantage.techindicators import TechIndicators

def ema(stock_symbol, api_key, period):
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # ema tim period eg 5 = 150 on 30 mins time frame
    p = period

    # ema
    data_ema, meta_data_ema = ti.get_ema(
        symbol=stock_symbol,
        series_type='close',
        interval='1min',
        time_period=p,
        )

    return data_ema

print(500/5)
