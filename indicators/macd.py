from alpha_vantage.techindicators import TechIndicators



def macd(stock_symbol, api_key):
    # variable for indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    # ema
    data_macd, meta_data_ema = ti.get_macd(
        symbol=stock_symbol,
        series_type='close',
        interval='30min',
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



def macd_ema(stock_symbol, api_key, fast, slow):
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
    previous_ema_slow = data_ema_slow['EMA'].iloc[-2]
    previous_ema_fast = data_ema_fast['EMA'].iloc[-2]

    current_macd_ema = current_ema_fast - current_ema_slow
    previous_macd_ema = previous_ema_fast - previous_ema_slow

    return current_macd_ema, previous_macd_ema




# macd('GBPUSD', 'GMQ2WJ9QWT993MVD')

print(macd_ema('EURUSD', '4OKNDHHTQH2CFWZ9', 12, 26))
