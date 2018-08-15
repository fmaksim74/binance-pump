#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from binance.client import Client
from binance.helpers import interval_to_milliseconds
import bncenums
from math import floor
from pgdb import BinanceDB
from queue import Queue
import threading
from time import sleep
from time import time
from tthread import TerminatableThread

class RequestQueue(TerminatableThread):

    queue = None
    queue_size = 2000
    klines = [ v // 1000 for v in [interval_to_milliseconds(v) for v in bncenums.kline_intervals] if v is not None]
    count = 0
    
    def __init__(self, q_size=2000):
        threading.Thread.__init__(self)
        RequestQueue.count += 1
        self._thread_id = RequestQueue.count
        self._tname = 'Thread {} is {}'.format(self._thread_id, type(self))
        if RequestQueue.queue is None:
            RequestQueue.queue = Queue(q_size)
            RequestQueue.queue_size = q_size
    
class RequestQueueLoader(RequestQueue):

    def run(self):
        print(self._tname, 'started')
        while  True:
            t = time()
            if (t - int(t)) == 0:
                break
        while not TerminatableThread.terminate:
            m = int(0)
            t = int(time())
            for i,vs in enumerate(RequestQueue.klines):
                if t - (t // vs) * vs == 0:
                    m += 1 << i
            if m > 0:
                RequestQueue.queue.put(m)
                print('Queue size:', RequestQueue.queue.qsize())
            sleep(1)
        print(self._tname, 'stoped')

class RequestQueueWorker(RequestQueue):

    client = None
    exchange_info = None
    dataQueue = None

    def run(self):
        print(self._tname, 'started')
        self.__klinesf = [ self.__1mTasks, self.__3mTasks, self.__5mTasks, self.__15mTasks, self.__30mTasks,
                           self.__1hTasks, self.__2hTasks, self.__4hTasks, self.__6hTasks, self.__8hTasks, self.__12hTasks,
                           self.__1dTasks, self.__3dTasks, self.__1wTasks ]
        if RequestQueueWorker.client is None:
            RequestQueueWorker.client = Client('','')
            if RequestQueueWorker.exchange_info is None:
                RequestQueueWorker.exchange_info = RequestQueueWorker.client.get_exchange_info()
        if RequestQueueWorker.dataQueue is None:
           RequestQueueWorker.dataQueue = Queue(RequestQueue.queue_size)
        while not TerminatableThread.terminate:
            try:
                q_item = RequestQueue.queue.get()
            except queue.Empty:
                pass
            else:
                data = self.__1sTasks()
                for i,vs in enumerate(RequestQueue.klines):
                    if q_item & ( 1 << i ):
                        self.__klinesf[i](data)
        print(self._tname, 'stoped')

    def __1sTasks(self, *args):
        t = time()
        print(self._tname, 'start doing 1s tasks with')
        r = RequestQueueWorker.client.get_server_time()
        r['ticker_price'] = RequestQueueWorker.client.get_symbol_ticker()
        print(self._tname, 'finished doing 1s tasks. Elapsed time =', time() - t)
        return r

    def __1mTasks(self, *args):
        t = time()
        print(self._tname, 'start doing 1m tasks')
        args[0]['order_book_ticker'] = RequestQueueWorker.client.get_orderbook_ticker()
        args[0]['kline1m'] = self.__LoadKLines('1m')
        print(self._tname, 'finished doing 1m tasks. Elapsed time =', time() - t)

    def __3mTasks(self, *args):
        pass
    def __5mTasks(self, *args):
        pass
    def __15mTasks(self, *args):
        pass
    def __30mTasks(self, *args):
        pass
    def __1hTasks(self, *args):
        pass
    def __2hTasks(self, *args):
        pass
    def __4hTasks(self, *args):
        pass
    def __6hTasks(self, *args):
        pass
    def __8hTasks(self, *args):
        pass
    def __12hTasks(self, *args):
        pass

    def __1dTasks(self, *args):
        t = time()
        print(self._tname, 'start doing 1d tasks')
        args[0]['ticker24hr'] = RequestQueueWorker.client.get_tiker()
        print(self._tname, 'finished doing 1d tasks. Elapsed time =', time() - t)

    def __3dTasks(self, *args):
        pass
    def __1wTasks(self, *args):
        pass

    def __LoadKLines(self, interval):
        t = time()
        print(self._tname, 'start loading KLines')
        r = [RequestQueueWorker.client.get_klines(symbol=s['symbol'], interval=interval, limit=5) for s in RequestQueueWorker.exchange_info['symbols']]
        print(self._tname, 'finished loading KLines. Elapsed time =', time() - t)
        return r

    def __LoadDepth(self):
        t = time()
        print(self._tname, 'start loading Depths')
        r = [RequestQueueWorker.client.get_order_book(symbol=s['symbol']) for s in RequestQueueWorker.exchange_info['symbols']]
        print(self._tname, 'finished loading Depths. Elapsed time =', time() - t)
        return r

################################################################################
# MAIN 
################################################################################
if __name__ == '__main__':
    for _ in range(11): RequestQueueWorker(2000).start()
    RequestQueueLoader().start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            TerminatableThread.terminate = True
            while threading.active_count() > 1:
                sleep(1)
            break
