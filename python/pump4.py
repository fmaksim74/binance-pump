#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from binance.client import Client
from binance.websockets import BinanceSocketManager
from bncenums import enum_kline_intervals
from pgdb import BinanceDB

def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)

def process_m_message(msg):
    spl1 =  msg['stream'].split(sep='@')
    spl2 = spl1[1].split(sep='_')
    msg.__setitem__('stream', { 'symbol': spl1[0], 'type': spl2[0], 'subtype': spl2[1] })
#   print("stream: {} data: {}\n".format(msg['stream'], msg['data']))
    bd.wssSaveMsg(msg)

if __name__ == '__main__':
    bc = Client('','')
    bd = BinanceDB()
    exchinf = bc.get_exchange_info()
#   bd.UpdateCommonSchema(exchinf)
#   bd.UpdateSymbolSchema(exchinf)
    trades   = ['{symbol}@trade'.format(symbol=s['symbol'].lower()) for s in exchinf['symbols']]
    klines = [['{symbol}@kline_{interval}'.format(symbol=s['symbol'].lower(),interval=kl) for s in exchinf['symbols']] for kl in enum_kline_intervals]
    minitickers = '!miniTicker@arr'
    tickers = '!ticker@arr'
    wss_data = trades + klines + [ minitickers , tickers ]
    print(wss_data)
    
    bm = BinanceSocketManager(bc)
#   # start any sockets here, i.e a trade socket
    conns = [ bm.start_multiplex_socket(d, process_m_message) for d in wss_data ]
#   conn_key1 = bm.start_multiplex_socket(trade_list, process_m_message)
#   conn_key2 = bm.start_multiplex_socket(klines1m, process_m_message)
#   conn_key3 = bm.start_multiplex_socket(klines3m, process_m_message)
#   conn_key4 = bm.start_multiplex_socket(klines5m, process_m_message)
#   # then start the socket manager
#   bm.start()


