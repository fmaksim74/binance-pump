#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import requests

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

if __name__ == '__main__':
    exit()
