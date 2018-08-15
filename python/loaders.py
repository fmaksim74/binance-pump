#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import time
import json
from pprint import pprint
import sys
import re
import requests
import psycopg2
import threading

class BinanceLoader(threading.Thread):
    
    terminate = False

    @staticmethod
    def LoaderByClassName(classname, br, bd, parms=None):
        if classname=='PriceLoader': return PriceLoader(br,bd,parms=parms)
        if classname=='KLineLoader': return KLineLoader(br,bd,parms=parms)
        if classname=='TradesLoader': return TradesLoader(br,bd,parms=parms)

    def __init__(self, br, bd, parms=None):
        threading.Thread.__init__(self)
        self.name = "BinanceLoader"
        self.br = br
        self.bd = bd
        self.parms = parms

class PriceLoader(BinanceLoader):

    def run(self):
        prev_data = dict()
        while not type(self).terminate:
            t = time.time()
            curr_data = self.br.get_all_tickers()
            if curr_data is not None:
                for d in curr_data:
                    if not ((d['symbol'] in prev_data) and (d['price'] == prev_data[d['symbol']])):
                        prev_data[d['symbol']] = d['price']
                        self.bd.InsertPrice(None, d)
            t = time.time() - t
            if t < 1:
#               print('PriceLoader paused for {} seconds'.format(str(t)))
                time.sleep(t)

class KLineLoader(BinanceLoader):

    def run(self):
        if self.parms is not None:
            if 'interval' in self.parms:
                i = IntervalToSecond(self.parms['interval'])
            while not type(self).terminate:
                t = time.time()
                for s in self.br.GetExchangeInfo()['symbols']:
                    self.parms['symbol'] = s['symbol']
                    self.bd.InsertKLine(self.parms, self.br.GetKLine(self.parms))
                    time.sleep(0.1)
                t = time.time() - t
                if t < i:
                    print('KLineLoader for interval {} paused for {}'.format(self.parms['interval'],str(i-t)))
                    time.sleep(i - t)

class TradesLoader(BinanceLoader):

    def run(self):
        last_id = dict()
        while not type(self).terminate:
            t = time.time()
            for s in self.br.GetExchangeInfo()['symbols']:
                s = s['symbol']
                self.parms['symbol'] = s
                curr_data = self.br.GetTrades(self.parms)
                if curr_data is not None:
                    for d in curr_data:
                        _id = int(d['id'])
                        if not((s in last_id) and (_id <= last_id[s])):
                            last_id[s] = _id
                            self.bd.InsertTrades(self.parms, d)
#               time.sleep(0.1)
            t = time.time() - t
            if t < 60:
                print('TradesLoader paused for {} seconds'.format(str(60-t)))
                time.sleep(60-t)

# ----------------------------------------------------------------------------------------------------------------------
# Main Section
if __name__ == '__main__':
    with BinanceDB() as bd:
        with BinanceRestAPI() as br:
            bd.SaveSymbols(br.GetExchangeInfo())
#           PriceLoader().start()
            TradesLoader({ 'symbol': 'ETCBTC', 'limit': 70 }).start()
#           for i in kline_intervals:
#           KLineLoader({ 'interval': '1m', 'limit': 10 }).start()
#           KLineLoader({ 'interval': '1h', 'limit': 10 }).start()
#           KLineLoader({ 'interval': '1d', 'limit': 10 }).start()
            print('Threads started:', threading.active_count())
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    BinanceLoader.terminate = True
                    while threading.active_count() > 1:
                        time.sleep(1)
                    break
#           parms = { 'symbol': 'ETCBTC', 'limit': 10 }
#           bd.InsertTrades(parms, br.GetTrades(parms))
#           parms = { "symbol": "ETHBTC" }
#           bd.InsertPrice(parms, br.GetPrice(parms))
#           parms = { 'symbol': 'ETCBTC', 'interval': '1m', 'limit': 10 }
#           bd.InsertKLine(parms, br.GetKLine(parms))
#           parms = { 'symbol': 'ETCBTC', 'limit': 10 }
#           bd.InsertKLine(parms, br.GetKLine(parms))

#           print(br.GetDepth({ "symbol": "ETHBTC", "limit": 5 }))


