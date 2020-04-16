from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import datetime

# variable for timeseries
ts = TimeSeries(key='E47X6GN73CIDKMOW', output_format='pandas')
# variable for indicator
ti = TechIndicators(key='FO8NGR3KQW03M9K2', output_format='pandas')
# data1, meta_data1 = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data_p, meta_data_p = ts.get_quote_endpoint(symbol='MSFT')
data_sma, meta_data_sma = ti.get_sma(symbol='MSFT', interval='weekly', time_period=60)
data_rsi, meta_data_rsi = ti.get_rsi(symbol='MSFT', interval='weekly', time_period=60)
data_bb, meta_data_bb = ti.get_bbands(symbol='MSFT', interval='weekly', time_period=60)

def stock_price():
    price = float(data_p['05. price'])
    # print('Price = ' + str((price)))
    return float(price)

def sma():
    # getting todays date for the dataframe
    date = datetime.today().strftime('%Y-%m-%d')
    # passing the date into the 'at' search
    sma = data_sma.at['2019-03-15', 'SMA']
    # getting the most current value aka the tail
    current_sma = float(sma)
    # print('SMA = ' + str(current_sma))
    return (current_sma)

def rsi():
    # getting todays date for the dataframe
    date = datetime.today().strftime('%Y-%m-%d')
    # passing the date into the 'at' search
    rsi = data_rsi.at['2019-03-15', 'RSI']
    # getting the most current value aka the tail
    current_rsi = float(rsi)
    # print('RSI = ' + str(current_rsi))
    return (current_rsi)

def bb():
    # getting todays date for the dataframe
    date = datetime.today().strftime('%Y-%m-%d')
    # passing the date into the 'at' search
    upper_bb = data_bb.at[date, 'Real Upper Band']
    middle_bb = data_bb.at[date, 'Real Middle Band']
    lower_bb = data_bb.at[date, 'Real Lower Band']
    # getting the most current value aka the first element of each bb
    current_upper_bb = upper_bb[0]
    current_middle_bb = middle_bb[0]
    current_lower_bb = lower_bb[0]
    # print(
    #     'Upper BB = ' + str(current_upper_bb) + '\n' +
    #     'middle BB = ' + str(current_middle_bb) + '\n' +
    #     'lower BB = ' + str(current_lower_bb)
    #     )
    return current_lower_bb, current_middle_bb, current_upper_bb

def stock_price_vs_sma_rsi():
    if(rsi() <= 60):
        print (stock_price())
        print (sma())
        print(rsi())
        print ('buy')
    else:
        print (stock_price())
        print (sma())
        print(rsi())
        print ('dont buy')




stock_price_vs_sma_rsi()
# stock_price()
sma()
rsi()
# bb()















# data.plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
# plt.title('BBbands indicator for  MSFT stock (60 min)')
# plt.show()


# API key is: E47X6GN73CIDKMOW
# API key is: FO8NGR3KQW03M9K2
