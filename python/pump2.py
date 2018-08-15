#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from binance.client import Client
from pgdb import BinanceDB
from bncenums import *
#from loaders import BinanceLoader
#import threading
#import time

with BinanceDB() as bd:
    bc = Client('' ,'')
    exch = bc.get_exchange_info()
    bd.UpdateCommonScheme(exch)
    bd.UpdateSymbolScheme(exch)
#   params = { 'symbol': 'ETHBTC', 'limit': 500 }
#   data = bc.get_order_book(**params)
#   bd.restSaveDepth(params, data)
#   data = bc.get_recent_trades(**params)
#   bd.restSaveTrades(params, data)
#   params = { 'symbol': 'ETHBTC' }
#   data = bc.get_historical_trades(**params)
#   bd.restSaveTrades(params, data)
#   data = bc.get_aggregate_trades(**params)
#   bd.restSaveAggTrades(params, data)
#   params = { 'symbol': 'ETHBTC', 'interval': '1m', 'limit': 10 }
#   data = bc.get_klines(**params)
#   bd.restSaveKLine(params, data)
#   params = { 'symbol': 'ETHBTC' }
#   data = bc.get_ticker(**params)
#   bd.restSave24hrTicker(params, data)
#   data = bc.get_ticker()
#   bd.restSave24hrTicker(None, data)
#   params = { 'symbol': 'ETHBTC' }
#   data = bc.get_symbol_ticker(**params)
#   bd.restSavePrice(params, data)
#   data = bc.get_symbol_ticker()
#   bd.restSavePrice(None, data)
    bd.Commit()
