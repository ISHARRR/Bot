import bot
import oanda


# to run the various currencies enter " python -c 'import fx; fx.eurusd()' "


def eurusd_ema():
    bot.ema('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')
def gbpusd_ema():
    bot.ema('GBPUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'GBP_USD')
def gbpjpy_ema():
    bot.ema('GBPJPY', 0.01, 'ARA2JDHJFGRI89VB', 'GBP_JPY')


def eurusd_macd():
    bot.macd('EURUSD', 0.0001, 'GMQ2WJ9QWT993MVD', 'EUR_USD')
def gbpusd_macd():
    bot.macd('GBPUSD', 0.0001, 'U6V8MKZWYAU0J728', 'GBP_USD')
def gbpjpy_macd():
    bot.macd('GBPJPY', 0.01, '3WBPOX3KVTFMVJ3P', 'GBP_JPY')
