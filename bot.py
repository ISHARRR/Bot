from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import matplotlib
import matplotlib.pyplot as plt
import os

# variable for timeseries
ts = TimeSeries(key='E47X6GN73CIDKMOW', output_format='pandas')
# variable for indicator
ti = TechIndicators(key='E47X6GN73CIDKMOW', output_format='pandas')
# data1, meta_data1 = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data_p, meta_data1 = ts.get_quote_endpoint(symbol='AAPL')
data, meta_data = ti.get_sma(symbol='AAPL', interval='1min', time_period=120)

def data_described():
    data.plot()
    # plt.show()
    print(data)

def stock_price():
    price = float(data_p['05. price']['Global Quote'])
    print('Price = ' + str((price)))


data_described()
stock_price()

# data.plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
# plt.title('BBbands indicator for  MSFT stock (60 min)')
# plt.show()
#
#
#
#
#
# API key is: E47X6GN73CIDKMOW
