from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import datetime

# variable for timeseries
ts = TimeSeries(key='E47X6GN73CIDKMOW', output_format='pandas')
# variable for indicator
ti = TechIndicators(key='E47X6GN73CIDKMOW', output_format='pandas')
# data1, meta_data1 = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data_p, meta_data_p = ts.get_quote_endpoint(symbol='AAPL')
data_sma, meta_data_sma = ti.get_sma(symbol='AAPL', interval='1min', time_period=120)

def stock_price():
    price = float(data_p['05. price'])
    print('Price = ' + str((price)))

def sma():
    # getting todays date for the dataframe
    date = datetime.today().strftime('%Y-%m-%d')
    # passing the date into the 'at' search
    sma = data_sma.at[date, 'SMA']
    # getting the most current value aka the tail
    current_sma = sma[-1]
    print('SMA = ' + str(current_sma))


stock_price()
sma()
















# data.plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
# plt.title('BBbands indicator for  MSFT stock (60 min)')
# plt.show()


# API key is: E47X6GN73CIDKMOW
