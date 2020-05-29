import bot



# to run the various currencies enter " python -c 'import fx; fx.eurusd()' "


def eurusd_ema():
    bot.trading_bot('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')
def gbpusd_ema():
    bot.trading_bot('GBPUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'GBP_USD')
def gbpjpy_ema():
    bot.trading_bot('GBPJPY', 0.01, 'ARA2JDHJFGRI89VB', 'GBP_JPY')


# def eurusd_macd():
#     bot.macd('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')
# def gbpusd_macd():
#     bot.macd('GBPUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'GBP_USD')
# def gbpjpy_macd():
#     bot.macd('GBPJPY', 0.01, 'ARA2JDHJFGRI89VB', 'GBP_JPY')


# 3WBPOX3KVTFMVJ3P
# U6V8MKZWYAU0J728
# GMQ2WJ9QWT993MVD

def test():
    bot.trading_bot_test('EURUSD', 0.0001, 'GMQ2WJ9QWT993MVD', 'EUR_USD')

def test1():
    bot.trading_bot_test1('EURUSD', 0.0001, 'U6V8MKZWYAU0J728', 'EUR_USD')

def test2():
    bot.trading_bot_test2('EURUSD', 0.0001, '3WBPOX3KVTFMVJ3P', 'EUR_USD')
