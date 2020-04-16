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

# --------- data structure

# ema
data_ema5, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='30min', time_period=5)
data_ema15, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='30min', time_period=15)

def ema():
    # getting todays date for the dataframe
    date = datetime.today().strftime('%Y-%m-%d')
    # passing the date into the 'at' search
    ema5 = data_ema5.at[date, 'EMA']
    ema15 = data_ema15.at[date, 'EMA']
    # getting the most current value aka the tail
    current_ema5 = ema5[0]
    current_ema15 = ema15[0]
    previous_ema5 = ema5[1]
    previous_ema15 = ema15[1]
    return current_ema5, current_ema15, previous_ema5, previous_ema15

    # -------------------------- tests
    # data_ema5.plot()
    # data_ema15.plot()
    # plt.show()
    # print('EMA = ' + str(current_ema5))
    # print('EMA = ' + str(current_ema15))
    # print('EMA p = ' + str(previous_ema5))
    # print('EMA p = ' + str(previous_ema15))

def main():

    while True:
        ema5, ema15, prv5, prv15 = ema()
        if (ema5 <= ema15) & (prv5 >= prv15): # BUY
            msg = EmailMessage()
            msg['Subject'] = 'BUY'
            msg['From'] = 'isharreehal8@gmail.com'
            msg['To'] = 'isharreehal8@gmail.com'
            msg.set_content('CHECK OVERALL TREND')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

                smtp.send_message(msg)

        if (ema5 >= ema15) & (prv5 <= prv15): # SELL
            msg = EmailMessage()
            msg['Subject'] = 'SELL'
            msg['From'] = 'isharreehal8@gmail.com'
            msg['To'] = 'isharreehal8@gmail.com'
            msg.set_content('CHECK OVERALL TREND')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

                smtp.send_message(msg)

        time.sleep(30)

main()








# main()
