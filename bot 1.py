from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from email.message import EmailMessage


import matplotlib
import matplotlib.pyplot as plt
import os
import time
import smtplib
import pytz

# variable for timeseries
ts = TimeSeries(key='E47X6GN73CIDKMOW', output_format='pandas')
# variable for indicator
ti = TechIndicators(key='FO8NGR3KQW03M9K2', output_format='pandas')


# --------- data structure

# ema
# data_ema, meta_data_ema = ts.get_intraday(symbol='USDEUR', interval='30min',outputsize='full')

def timezone():
    ny_timezone = pytz.timezone('America/New_york')
    datetime_NY = datetime.now(ny_timezone)
    return (datetime_NY.strftime("%H:%M:%S"))

def ema():
    data_ema5, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='1min', time_period=450)
    data_ema15, meta_data_ema = ti.get_ema(symbol='USDEUR', interval='1min', time_period=150)
    
    # getting the most current value aka the n (tail)
    current_ema5 = data_ema5['EMA'].iloc[-1]
    current_ema15 = data_ema15['EMA'].iloc[-1]
    # getting the second most current value aka the n-1
    previous_ema5 = data_ema5['EMA'].iloc[-16]
    previous_ema15 = data_ema15['EMA'].iloc[-16]

    return current_ema5, current_ema15, previous_ema5, previous_ema15

    # -------------------------- tests
    # data_ema['4. close'].plot()
    # data_ema15.plot()
    # plt.plot(data_ema5, 'b')
    # plt.plot(data_ema15, 'r')
    # plt.show()

    # print('EMA = ' + str(current_ema5))
    # print('EMA = ' + str(current_ema15))
    # print('EMA p = ' + str(previous_ema5))
    # print('EMA p = ' + str(previous_ema15))

def main():
    print('Running...')
    while True:
        ema5, ema15, prv5, prv15 = ema()
        ny_time = timezone()
        print ('5 =', ema5, '15 =', ema15, 'p5 =', prv5, 'p15 =', prv15, '  Time:', ny_time)
        if (ema5 > ema15) and (prv5 < prv15): # BUY
            print('BUY: USD-EUR', )
            msg = EmailMessage()
            msg['Subject'] = 'BUY: USD - EUR'
            msg['From'] = 'isharreehal8@gmail.com'
            msg['To'] = 'isharreehal8@gmail.com'
            msg.set_content('CHECK OVERALL TREND')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

                smtp.send_message(msg)

        if (ema5 < ema15) and (prv5 > prv15): # SELL
            print('SELL: USD - EUR')
            msg = EmailMessage()
            msg['Subject'] = 'SELL: USD-EUR'
            msg['From'] = 'isharreehal8@gmail.com'
            msg['To'] = 'isharreehal8@gmail.com'
            msg.set_content('CHECK OVERALL TREND')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

                smtp.send_message(msg)

        time.sleep(300)

main()