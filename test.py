import oanda



account = '101-004-14591208-007'

cross = oanda.Oanda(account, "GDPUSD", 0.001, 0.95)

if cross.get_open_trade_count() < 1:
    print('do this')

else:
    print('thsi')
