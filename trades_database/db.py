import shelve


def updateDB(buyorsell, data, file):
    d = shelve.open(file, writeback=True)

    try:
        if buyorsell == 'BUY':
            d['buy_id'] = data
            return d['buy_id']
        elif buyorsell == 'SELL':
            d['sell_id'] = data
            return d['sell_id']
    finally:
        d.close()

def getDB(buyorsell, file):
    d = shelve.open(file, writeback=True)

    try:
        if buyorsell == 'BUY':
            return d['buy_id']
        elif buyorsell == 'SELL':
            return d['sell_id']
    finally:
        d.close()


# updateDB('BUY', 0, 'smacrossDB')
# updateDB('SELL', 0, 'smacrossDB')
#
# print(getDB('BUY', 'smacrossDB'))
