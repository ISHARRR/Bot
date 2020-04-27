from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from email.message import EmailMessage


import matplotlib
import matplotlib.pyplot as plt
import os
import time
import smtplib

    # variable for timeseries
ts = TimeSeries(key='E47X6GN73CIDKMOW', output_format='pandas')
    # variable for indicator
ti = TechIndicators(key='FO8NGR3KQW03M9K2', output_format='pandas')

# data_ema, meta_data_ema = ts.get_intraday(symbol='USDEUR', interval='30min',outputsize='full')

data_ema5, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='1min', time_period=450)
data_ema15, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='1min', time_period=150)
    
plt.plot(data_ema5, 'b')
plt.plot(data_ema15, 'r')
plt.gca().invert_yaxis()
plt.show()
   
    