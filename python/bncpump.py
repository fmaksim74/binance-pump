#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from time import sleep
from binance.client import Client
from binance.websockets import BinanceSocketManager
from bncenums import enum_kline_intervals
from bncpgdb import BinanceDB
import sys

if __name__ == '__main__':

    bc = Client('','')
    bd = BinanceDB()
    exchinf = bc.get_exchange_info()
    bd.UpdateCommonSchema(exchinf)
    bd.UpdateSymbolSchema(exchinf)
    trades   = ['{symbol}@trade'.format(symbol=s['symbol'].lower()) for s in exchinf['symbols']]
    klines = [['{symbol}@kline_{interval}'.format(symbol=s['symbol'].lower(),interval=kl) for s in exchinf['symbols']] for kl in enum_kline_intervals]
    minitickers = '!miniTicker@arr'
    tickers = '!ticker@arr'
#   wss_data = [ trades, ] + klines + [ minitickers , tickers ]
    wss_data = klines
    
    bm = BinanceSocketManager(bc)
    # start any sockets here, i.e a trade socket
    conns = [ bm.start_multiplex_socket(d, bd.wssSaveMsg) for d in wss_data ]
    # then start the socket manager
    bm.daemon = True
    bm.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        for conn in conns:
            bm.stop_socket(conn)
    finally:
        print('Stopped')



