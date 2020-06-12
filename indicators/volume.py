from alpha_vantage.foreignexchange import ForeignExchange


def volume(stock_symbol, api_key):
    first_curr, second_curr = stock_symbol[:len(stock_symbol)//2], stock_symbol[len(stock_symbol)//2:]
    # 100 day period sma = 600 and 200 = 1200
    # variable for indicator
    fx = ForeignExchange(key=api_key, output_format='pandas')
    # sma
    data_vol, meta_data_vol = fx.get_daily(symbol=stock_symbol, outputsize='compact')
    # getting the most current value aka the n (tail)
    current_vol = data_vol['5. volume'].iloc[-1]
    # return current_sma200
    return current_vol
#
# print(volume('EURUSD', 'ARA2JDHJFGRI89VB'))
