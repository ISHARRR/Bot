from alpha_vantage.techindicators import TechIndicators



def macd(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # ema
    data_macd, meta_data_ema = ti.get_macd(
        symbol=stock_symbol,
        series_type='close',
        interval='5min',
        fastperiod=12,
        slowperiod=26,
        signalperiod=9
    )

    # getting the most current value aka the n (tail)
    current_macd = data_macd['MACD'].iloc[-1]
    current_macd_signal = data_macd['MACD_Signal'].iloc[-1]
    # current_macd_hist = data_macd['MACD_Hist'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_macd = data_macd['MACD'].iloc[-7]
    previous_macd_signal = data_macd['MACD_Signal'].iloc[-7]
    # previous_macd_hist = data_macd['MACD_Hist'].iloc[-16]

    return current_macd, current_macd_signal, previous_macd, previous_macd_signal

# macd('GBPUSD', 'GMQ2WJ9QWT993MVD')
