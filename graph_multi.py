from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from email.message import EmailMessage


import matplotlib
import matplotlib.pyplot as plt
import os
import time
import smtplib



def ema_graph(stock_symbol, api_key):

    # variable for indicator
    ti = TechIndicators(key = api_key, output_format='pandas')

    data_ema5, meta_data_ema = ti.get_ema(symbol = stock_symbol, interval='1min', time_period=450)
    data_ema15, meta_data_ema = ti.get_ema(symbol = stock_symbol, interval='1min', time_period=150)
    
    plt.plot(data_ema5, 'b')
    plt.plot(data_ema15, 'r')
    #plt.gca().invert_yaxis()
    plt.title(stock_symbol)
    plt.show()
    
def main():
    # 1
    ema_graph('SPX', 'E47X6GN73CIDKMOW')
    # 2
    #ema_graph('USDEUR', 'F34FEQKDQI3J2AKI')
    # 3
    #ema_graph('USDGBP', 'ARA2JDHJFGRI89VB')
    # 4
    #ema_graph('TSLA', '60I75BKCK0OFGNKA')
    # 5
    
main()
    

   
    
