# from sys import platform


import shelve
import pathlib


def checkDB(file):
    db = pathlib.Path(file + '.db').exists()
    bak = pathlib.Path(file + '.bak').exists()
    dat = pathlib.Path(file + '.dat').exists()
    dirr = pathlib.Path(file + '.dir').exists()

    if bak or dat or dirr or db:
        return True


def getDB(buyorsell, file):
    if checkDB(file):
        with shelve.open(file) as d:
            if buyorsell == 'BUY':
                id = d['key']['buy_id']
                return id
            elif buyorsell == 'SELL':
                id = d['key']['sell_id']
                return id


def createDB(file, id, direction):
    if checkDB(file):
        pass
    else:
        buy_id = 0
        sell_id = 0

        if direction == 'LONG':
            buy_id = id
        elif direction == 0:
            buy_id

        if direction == 'SHORT':
            sell_id = id
        elif direction == 0:
            sell_id

        with shelve.open(file) as d:
            d['key'] = {'buy_id': buy_id, 'sell_id': sell_id}

    # if platform == 'linux':
    #     if bak or dat or dirr:
    #         pass
    #     else:
    #         with shelve.open(file) as d:
    #             d['key'] = {'buy_id': buy_id, 'sell_id': sell_id}
    # elif platform == 'darwin' or platform == 'linux2':
    #     if db:
    #         pass
    #     else:
    #         with shelve.open(file) as d:
    #             d['key'] = {'buy_id': buy_id, 'sell_id': sell_id}


def updateDB(buyorsell, data, file):
    if checkDB(file):
        with shelve.open(file, writeback=True) as d:
            if buyorsell == 'BUY':
                d['key']['buy_id'] = data
                id = d['key']['buy_id']
                return id
            elif buyorsell == 'SELL':
                d['key']['sell_id'] = data
                id = d['key']['sell_id']
                return id


# createDB('crossDB')
# print(getDB('BUY', 'adx_directDB'))
# print(getDB('SELL', 'adx_directDB'))
# print(updateDB('BUY', 111, 'crossDB'))
# print(updateDB('SELL', 0, 'crossDB'))
# print(updateDB('BUY', 51, 'smacrossDB'))
# print(updateDB('SELL', 0, 'smacrossDB'))
#
# print(getDB('BUY', 'crossDB'))
