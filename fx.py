import bot


# to run the various currencies enter " python -c 'import fx; fx.eurusd()' "


def eurusd():
    bot.trade('EURUSD', 0.0001,'4OKNDHHTQH2CFWZ9', 'EUR_USD')

def gbpusd():
    bot.trade('GBPUSD', 0.0001,'T7NT8GKR7CJ36U3C', 'GBP_USD')

def gbpjpy():
    bot.trade('GBPJPY', 0.01,'ARA2JDHJFGRI89VB', 'GBP_JPY')
