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

# ----------------------------------------------------------------------------------------------------------------------
# Binance API

security_type  =  ('NONE','TRADE','USER_DATA','USER_STREAM','MARKET_DATA')
symbol_status  =  ('PRE_TRADING','TRADING','POST_TRADING','END_OF_DAY','HALT','AUCTION_MATCH','BREAK')
symbol_type  =  ('SPOT')
order_status  =  ('NEW','PARTIALLY_FILLED','FILLED','CANCELED','PENDING_CANCEL','REJECTED','EXPIRED')
order_type  =  ('LIMIT','MARKET','STOP_LOSS','STOP_LOSS_LIMIT','TAKE_PROFIT','TAKE_PROFIT_LIMIT','LIMIT_MAKER')
order_side  =  ('BUY','SELL')
time_in_force  =  ('GTC','IOC','FOK')
kline_intervals  =  ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w','1M')
rate_limiter  =  ('REQUESTS', 'ORDERS')
rate_limit_intervals  =  ('SECOND', 'MINUTE', 'DAY')
def IntervalToSecond(i_val=None):
    if isinstance(i_val, int):
        if i_val > len(kline_intervals) - 1: 
            i_val = None
        else:
            i_val = kline_intervals[i_val -1]
    if isinstance(i_val, str):
        i_num = int(i_val[:-1])
        i_unit = i_val[len(i_val)-1:]
        if i_unit == 'm':
            return i_num * 60
        elif i_unit == 'h':
            return i_num * 60 * 60
        elif i_unit == 'd':
            return i_num * 60 * 60 * 24
        elif i_unit == 'w':
            return i_num * 60 * 60 * 24 * 7
        elif i_unit == 'M':
            return i_num * 60 * 60 * 24 * 30
        else:
            return i_num * 60
    return 60

class BinanceRestAPI(object):
    u""" REST API implemetation for Binance.com """

    __base_url = 'http://api.binance.com'
    __session = requests.Session()
    __exchange_info = None

    def __init__(self):
        self.GetExchangeInfo()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__session is not None:
            self.__session.close()

    def Get(self, url, params=None):
        with self.__session.get(url, params=params) as r:
            if r.status_code == requests.codes.ok:
                return r.json()
            else:
                if r.status_code == requests.codes.too_many:
                    print("Got 429 error")
                return None

    def GetPing(self):
        u"""
        Test connectivity
        Parameters: none
        """
        return self.Get(self.__base_url+'/api/v1/ping')

    def GetServerTime(self):
        u"""
        Test connectivity to the Rest API and get the current server time.
        Parameters: NONE
        """
        return self.Get(self.__base_url+'/api/v1/time')['serverTime']

    def GetExchangeInfo(self):
        u"""
        Current exchange trading rules and symbol information
        Parameters: NONE
        """
        if type(self).__exchange_info is None:
            self.__exchange_info = self.Get(self.__base_url+'/api/v1/exchangeInfo')
        return self.__exchange_info

    def GetDepth(self, params=None):
        u"""
        Order book
        Parameters: { 'symbol': (STRING)[, 'limit': (INT) 5,10,20,50,100,500,1000 def 100] }
        """
        return self.Get(self.__base_url+'/api/v1/depth', params)

    def GetTrades(self, params=None):
        u"""
        Get recent trades (up to last 500).
        Parameters: { 'symbol': (STRING)[, 'limit': (INT) <= 500 def 500] }
        """
        return self.Get(self.__base_url+'/api/v1/trades', params)

    def GetHistoricalTrades(self, params=None):
        u"""
        Get older trades.
        Parameters: { 'symbol': (STRING)[, 'limit': (INT) <= 500 def 500][, 'fromId': (LONG)] }
        """
        return self.Get(self.__base_url+'/api/v1/historicalTrades', params)

    def GetAggTrades(self, params=None):
        u"""
        Get older trades.
        Parameters: { 'symbol': (STRING)[, 'fromId': (LONG)][, 'startTime': (LONG)][, 'endTime': (LONG)][, 'limit': (INT) <= 500 def 500] }
        """
        return self.Get(self.__base_url+'/api/v1/aggTrades', params)

    def GetKLine(self, params=None):
        u"""
        Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
        Parameters: { 'symbol': (STRING), 'interval': (ENUM)[, 'limit': (INT) <= 500 def 500][, 'startTime': (LONG)][, 'endTime': (LONG)] }
        """
        return self.Get(self.__base_url + '/api/v1/klines', params)

    def Get24hr(self, params=None):
        u"""
        24 hour price change statistics
        Parameters: { ['symbol': (STRING)] }
        """
        return self.Get(self.__base_url+'/api/v1/ticker/24hr', params)

    def GetPrice(self, params=None):
        u"""
        Latest price for a symbol or symbols.
        Parameters: { ['symbol': (STRING)] }
        """
        return self.Get(self.__base_url + '/api/v1/ticker/price', params)

    def GetBookTicker(self, params=None):
        u"""
        Best price/qty on the order book for a symbol or symbols.
        Parameters: { ['symbol': (STRING)] }
        """
        return self.Get(self.__base_url+'/api/v1/ticker/bookTicker', params)


class BinanceDB(object):

    __db_connection = None

    def __init__(self):
        self.Connect()
        self.__cursor = self.__db_connection.cursor()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__db_connection is not None:
            self.__db_connection.close()

    def Connect(self):
        if type(self).__db_connection is None:
            self.__db_connection = psycopg2.connect(dbname='binancedb', user='max', password='123', host='localhost')

    def SaveExchangeInfo(self, ei=None):
        self.__cursor.execute('SELECT "_Id" FROM "ServerInfo" WHERE "_Name" = \'Binance\';')
        r = self.__cursor.fetchall()
        if len(r) == 0:
            sql = 'INSERT INTO "ServerInfo"'+ \
                  '    ("_Name","_BaseUrl","_TimeZone","_RateLimits","_ExchangeFilters") '+ \
                  '  VALUES'+ \
                  '    (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\'); '+ \
                  'COMMIT;'
            self.__cursor.execute(sql.format('Binance','http://api.binance.com',ei['timezone'],json.dumps(ei['rateLimits']),json.dumps(ei['exchangeFilters'])))
        else:
            sql = 'UPDATE "ServerInfo"'+ \
                  '   SET "_RateLimits" = \'{}\', "_ExchangeFilters" = \'{}\' '+ \
                  'WHERE "_Id" = {}; '+ \
                  'COMMIT;'
            self.__cursor.execute(sql.format(json.dumps(ei['rateLimits']),json.dumps(ei['exchangeFilters']),1))

    def ReadServerInfo(self):
        if type(self).__server_info is None:
            self.__cursor.execute('SELECT "_Id", "_Name", "_TimeZone", "_BaseUrl" FROM "ExchangeInfo"."ServerInfo";')
            self.__server_info = dict()
            r = c.fetchall()
            if len(r) > 0:
                self.__server_info['_Id'] = r[0][0]
                self.__server_info['_Name'] = r[0][1]
                self.__server_info['_TimeZone'] = r[0][2]
                self.__server_info['_BaseUrl'] = r[0][3]
                print(self.__server_info)

    def CreatePriceTable(self, symbol):
        if len(symbol) > 0:
            sql = 'CREATE TABLE IF NOT EXISTS "price{S}" ('+ \
                  '    "_Time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,'+ \
                  '    "_Price" NUMERIC NOT NULL'+ \
                  ');'+ \
                  'COMMIT;'
            self.__cursor.execute(sql.format(S=symbol))

    def DropPriceTable(self, symbol):
        if len(symbol) > 0:
            self.__cursor.execute('DROP TABLE IF EXISTS "price{S}"; COMMIT;'.format(S=symbol))

    def InsertPrice(self, rparms, data):
        if isinstance(data, dict):
            l = list()
            l.append(data)
            data = l
        if isinstance(data, list):
            sql = 'INSERT INTO "price{S}" ("_Price") VALUES ({P}); COMMIT;'
            for d in data:
                self.__cursor.execute(sql.format(S=d['symbol'],P=d['price']))

    def CreateKLineTable(self, symbol, interval):
        if len(symbol) > 0:
            sql = 'CREATE TABLE IF NOT EXISTS "kline{S}_{I}" ('+ \
                  '    "_OpenTime" BIGINT NOT NULL PRIMARY KEY,'+ \
                  '    "_Open" NUMERIC,'+ \
                  '    "_High" NUMERIC,'+ \
                  '    "_Low"  NUMERIC,'+ \
                  '    "_Close" NUMERIC,'+ \
                  '    "_Volume" NUMERIC,'+ \
                  '    "_CloseTime" BIGINT,'+ \
                  '    "_QuoteAssetVolume" NUMERIC,'+ \
                  '    "_NumerOfTrades" BIGINT,'+ \
                  '    "_TakerByBaseAssetVolume" NUMERIC,'+ \
                  '    "_TakerBuyQuoteAssetVolume" NUMERIC,'+ \
                  '    "Ignore" NUMERIC'+ \
                  '); COMMIT;'+ \
                  'CREATE UNIQUE INDEX IF NOT EXISTS "kline{S}_{I}_OCT_IX" ON "kline{S}_{I}"'+ \
                  '    ("_OpenTime" ASC, "_CloseTime" ASC); COMMIT;'
            self.__cursor.execute(sql.format(S=symbol,I=interval))

    def DropKLineTable(self, symbol, interval):
        if len(symbol) > 0:
            self.__cursor.execute('DROP TABLE IF EXISTS "price{}"; COMMIT;'.format(symbol))

    def CreateKLineTables(self, symbol):
        if len(symbol) > 0:
            for i in kline_intervals:
                self.CreateKLineTable(symbol, i)

    def DropKLineTables(self, symbol):
        if len(symbol) > 0:
            for i in kline_intervals:
                self.DropKLineTable(symbol, i)

    def InsertKLine(self, rparms, data):
        if isinstance(data, list):
            sql = 'INSERT INTO "kline{S}_{I}"'+ \
                  '    ("_OpenTime","_Open","_High","_Low","_Close","_Volume","_CloseTime","_QuoteAssetVolume",'+ \
                       '"_NumerOfTrades","_TakerByBaseAssetVolume","_TakerBuyQuoteAssetVolume","Ignore")'+ \
                  'VALUES '+ \
                  '    ({D}); COMMIT;'
            for d in data:
                print(sql.format(S=rparms['symbol'],I=rparms['interval'],D=json.dumps(d).replace('"','').replace('[','').replace(']','')))
#               try:
#                   self.__cursor.execute(sql.format(S=rparms['symbol'],I=rparms['interval'],D=json.dumps(d).replace('"','').replace('[','').replace(']','')))
#               except psycopg2.IntegrityError:
#                   pass

    def CreateTradesTable(self, symbol):
        if len(symbol) > 0:
            sql = 'CREATE TABLE IF NOT EXISTS "trades{S}" ('+ \
                  '    "_Id" BIGINT NOT NULL PRIMARY KEY ,'+ \
                  '    "_Price" NUMERIC NOT NULL,'+ \
                  '    "_Qty" NUMERIC NOT NULL,'+ \
                  '    "_Time" NUMERIC NOT NULL,'+ \
                  '    "_IsBuyerMaker" BOOLEAN NOT NULL,'+ \
                  '    "_IsBestMatch" BOOLEAN NOT NULL'+ \
                  '); COMMIT;'
            self.__cursor.execute(sql.format(S=symbol))

    def DropTradesTable(self, symbol):
        if len(symbol) > 0:
            self.__cursor.execute('DROP TABLE IF EXISTS "trades{S}"; COMMIT;'.format(S=symbol))

    def InsertTrades(self, rparms, data):
        if rparms is None:
            return
        if isinstance(data, dict):
            l = list()
            l.append(data)
            data = l
        if isinstance(data, list):
            sql = 'INSERT INTO "trades{S}"'+ \
                  '    ("_Id","_Price","_Qty","_Time","_IsBuyerMaker","_IsBestMatch")'+ \
                  'VALUES'+ \
                  '    ({D});'+ \
                  'COMMIT;'
            for d in data:
                try:
                    self.__cursor.execute(sql.format(S=rparms['symbol'],D=json.dumps(list(d.values())).replace('"','').replace('[','').replace(']','')))
                except psycopg2.IntegrityError:
                    pass

    def SaveSymbols(self, ei=None, do_drop=False):
        if ei is not None:
            for s in ei['symbols']:
                if do_drop:
                    self.DropPriceTable(s['symbol'])
                    self.DropKLineTables(s['symbol'])
                    self.DropTradesTable(s['symbol'])
                self.CreatePriceTable(s['symbol'])
                self.CreateKLineTables(s['symbol'])
                self.CreateTradesTable(s['symbol'])


class BinanceLoader(threading.Thread):
    
    terminate = False

    def __init__(self, parms=None):
        threading.Thread.__init__(self)
        self.name = "BinanceLoader"
        self.br = BinanceRestAPI()
        self.bd = BinanceDB()
        self.parms = parms

class PriceLoader(BinanceLoader):

    def run(self):
        prev_data = dict()
        while not type(self).terminate:
            t = time.time()
            curr_data = self.br.GetPrice()
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
            PriceLoader().start()
            TradesLoader({ 'symbol': 'ETCBTC', 'limit': 70 }).start()
#           for i in kline_intervals:
            KLineLoader({ 'interval': '1m', 'limit': 10 }).start()
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


