import shelve


def updateDB(buyorsell, data, file):
    d = shelve.open(file, writeback=True)

    try:
        if buyorsell == 'BUY':
            d['buy_id'] = data
            return int(d['buy_id'])
        elif buyorsell == 'SELL':
            d['sell_id'] = data
            return int(d['sell_id'])
    finally:
        d.close()

def getDB(buyorsell, file):
    d = shelve.open(file, writeback=True)

    try:
        if buyorsell == 'BUY':
            return int(d['buy_id'])
        elif buyorsell == 'SELL':
            return int(d['sell_id'])
    finally:
        d.close()


# print(updateDB('BUY', 111, 'crossDB'))
# print(updateDB('BUY', 51, 'smacrossDB'))
# print(updateDB('SELL', 0, 'crossDB'))
# print(updateDB('SELL', 0, 'smacrossDB'))
#
# print(getDB('BUY', 'crossDB'))
