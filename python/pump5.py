#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from os import getpid
from time import time ,sleep
from multiprocessing import Process, Queue
from bncenums import kline_intervals, klines
from binance.helpers import interval_to_milliseconds
from binance.client import Client

def RequestProducer(queue):
    pid = getpid()
    print('RequestProducer in thread {} started'.format(pid))
    while  True:
        t = time()
        if (t - int(t)) == 0:
            break
    while True:
        queue.put(1)
        t = int(time())
        for i,vs in enumerate(klines):
            if t - (t // vs) * vs == 0:
                queue.put(1 << (i + 1))
        print('Queue size:', queue.qsize())
        sleep(1)
    print('RequestProducer in thread {} stoped'.format(pid))

def RequestConsumer(rqueue, client=None):
    pid = getpid()
    print('RequestConsumer in thread {} started'.format(pid))
    klinesf = [ __1sTasks, 
                __1mTasks, __3mTasks, __5mTasks, __15mTasks, __30mTasks,
                __1hTasks, __2hTasks, __4hTasks, __6hTasks, __8hTasks, __12hTasks,
                __1dTasks, __3dTasks, 
                __1wTasks ]
    if client is None: client = Client('','')
    while True:
        try:
            q_item = rqueue.get()
        except queue.Empty:
            pass
        else:
            for i,vs in enumerate(klines):
                m = ( 1 << i )
                if q_item & m:
                    data = client.get_server_time()
                    data['taskType'] = m
                    if m == 1: 
                        t_int = '1s'
                    else:
                        t_int = kline_intervals[i]
                    print('RequestConsumer in thread {} start doing {} tasks'.format(pid,t_int))
                    t = time()
                    klinesf[i](pid, data)
                    print('RequestConsumer in thread {} finished doing {} tasks. Elapsed time = {}'.format(pid,t_int, time() - t))
    print('RequestConsumer in thread {} stoped'.format(pid))
    
def __1sTasks(*args):
    if args[1] is not None:
        args[1]['data'] = {}
        args[1]['data']['ticker_price'] = client.get_symbol_ticker()

def __1mTasks(*args):
    if args[1] is not None:
        args[1]['data'] = {}
        args[1]['data']['order_book_ticker'] = client.get_orderbook_ticker()
        args[1]['data']['kline1m'] = __LoadKLines(kline_intervals[args[1]['taskType']], exchange_info)

def __3mTasks(*args):
    pass
def __5mTasks(*args):
    pass
def __15mTasks(*args):
    pass
def __30mTasks(*args):
    pass
def __1hTasks(*args):
    pass
def __2hTasks(*args):
    pass
def __4hTasks(*args):
    pass
def __6hTasks(*args):
    pass
def __8hTasks(*args):
    pass
def __12hTasks(*args):
    pass

def __1dTasks(*args):
    if args[1] is not None:
        args[1]['data'] = {}
        args[1]['data']['ticker24hr'] = client.get_tiker()

def __3dTasks(*args):
    pass
def __1wTasks(*args):
    pass

def __LoadKLines(interval, exch_inf):
    return [client.get_klines(symbol=s['symbol'], interval=interval, limit=5) for s in exch_inf['symbols']]

def __LoadDepth(exch_inf):
    return [client.get_order_book(symbol=s['symbol']) for s in exch_inf['symbols']]

################################################################################
# MAIN 
################################################################################
if __name__ == '__main__':
    queue = Queue(2000)
    client = Client('','')
    exchange_info = client.get_exchange_info()
    for i in range(11):
        Process(target=RequestConsumer, args=(queue,)).start()
        sleep(0.5)
    p = Process(target=RequestProducer, args=(queue,))
    p.start()
    p.join()
