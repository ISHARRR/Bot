import bot


# to run the various currencies enter " python -c 'import fx; fx.eurusd()' "


def eurusd():
    bot.trade('EURUSD', '4OKNDHHTQH2CFWZ9', 'EUR_USD')

def gbpjpy():
    bot.trade('GBPJPY', 'ARA2JDHJFGRI89VB', 'GBP_JPY')

def gbpusd():
    bot.trade('GBPUSD', 'T7NT8GKR7CJ36U3C', 'GBP_USD')
