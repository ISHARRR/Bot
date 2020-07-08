import bot


# to run the various currencies enter " python -c 'import fx; fx.eurusd()' "


def eurusd():
    bot.adx_ema_sl_bot('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')


def gbpusd():
    bot.adx_ema_sl_bot('GBPUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'GBP_USD')


def gbpjpy():
    bot.adx_ema_sl_bot('GBPJPY', 0.01, 'ARA2JDHJFGRI89VB', 'GBP_JPY')


# def eurusd_macd():
#     bot.macd('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')
# def gbpusd_macd():
#     bot.macd('GBPUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'GBP_USD')
# def gbpjpy_macd():
#     bot.macd('GBPJPY', 0.01, 'ARA2JDHJFGRI89VB', 'GBP_JPY')


# 3WBPOX3KVTFMVJ3P
# U6V8MKZWYAU0J728
# GMQ2WJ9QWT993MVD


def adx_cross():
    bot.adx_crossover_bot('EURUSD', 0.0001, '4OKNDHHTQH2CFWZ9', 'EUR_USD')


def adx_test():
    bot.adx_test_bot('EURUSD', 0.0001, 'ARA2JDHJFGRI89VB', 'EUR_USD')


def adx_ts():
    bot.adx_crossover_bot('EURUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'EUR_USD')


def adx_ema_sl():
    bot.adx_ema_sl_bot('EURUSD', 0.0001, 'T7NT8GKR7CJ36U3C', 'EUR_USD')


def cross():
    bot.crossover_bot('EURUSD', 0.0001, 'GMQ2WJ9QWT993MVD', 'EUR_USD')


def sma_cross():
    bot.sma_crossover_bot('EURUSD', 0.0001, 'U6V8MKZWYAU0J728', 'EUR_USD')


def test():
    bot.test('GBPJPY', 0.0001, 'U6V8MKZWYAU0J728', 'GBP_JPY')
