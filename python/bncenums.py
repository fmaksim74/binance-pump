#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from binance.enums import *
from binance.helpers import interval_to_milliseconds

#-----------------------------------------------------------------------------------------------------------------------
enum_kline_intervals = (KLINE_INTERVAL_1MINUTE,KLINE_INTERVAL_3MINUTE,KLINE_INTERVAL_5MINUTE,KLINE_INTERVAL_15MINUTE, \
                        KLINE_INTERVAL_30MINUTE,KLINE_INTERVAL_1HOUR,KLINE_INTERVAL_2HOUR,KLINE_INTERVAL_4HOUR, \
                        KLINE_INTERVAL_6HOUR,KLINE_INTERVAL_8HOUR,KLINE_INTERVAL_12HOUR,KLINE_INTERVAL_1DAY, \
                        KLINE_INTERVAL_3DAY,KLINE_INTERVAL_1WEEK,KLINE_INTERVAL_1MONTH)

klines = [ v // 1000 for v in [interval_to_milliseconds(v) for v in enum_kline_intervals] if v is not None]
#-----------------------------------------------------------------------------------------------------------------------
enum_order_side = (SIDE_BUY,SIDE_SELL)
#-----------------------------------------------------------------------------------------------------------------------
enum_order_status = (ORDER_STATUS_NEW,ORDER_STATUS_PARTIALLY_FILLED,ORDER_STATUS_FILLED,ORDER_STATUS_CANCELED, \
                     ORDER_STATUS_PENDING_CANCEL,ORDER_STATUS_REJECTED,ORDER_STATUS_EXPIRED)
#-----------------------------------------------------------------------------------------------------------------------
enum_order_type = (ORDER_TYPE_LIMIT,ORDER_TYPE_MARKET,ORDER_TYPE_STOP_LOSS,ORDER_TYPE_STOP_LOSS_LIMIT, \
                   ORDER_TYPE_TAKE_PROFIT,ORDER_TYPE_TAKE_PROFIT_LIMIT,ORDER_TYPE_LIMIT_MAKER)
#-----------------------------------------------------------------------------------------------------------------------
RATE_LIMITER_REQUESTS = 'REQUEST'
RATE_LIMITER_ORDERS   = 'ORDERS'
enum_rate_limiter = (RATE_LIMITER_REQUESTS ,RATE_LIMITER_ORDERS)
#-----------------------------------------------------------------------------------------------------------------------
RATE_LIMIT_INTERVAL_SECOND = 'SECOND'
RATE_LIMIT_INTERVAL_MINUTE = 'SECOND'
RATE_LIMIT_INTERVAL_DAY    = 'SECOND'
enum_rate_limit_intervals  =  (RATE_LIMIT_INTERVAL_SECOND,RATE_LIMIT_INTERVAL_MINUTE,RATE_LIMIT_INTERVAL_DAY)
#-----------------------------------------------------------------------------------------------------------------------
SECURITY_TYPE_NONE        = 'NONE'
SECURITY_TYPE_TRADE       = 'TRADE'
SECURITY_TYPE_USER_DATA   = 'USER_DATA'
SECURITY_TYPE_USER_STREAM = 'USER_STREAM'
SECURITY_TYPE_MARKET_DATA = 'MARKET_DATA'
enum_security_type  =  (SECURITY_TYPE_NONE,SECURITY_TYPE_TRADE,SECURITY_TYPE_USER_DATA,SECURITY_TYPE_USER_STREAM, \
                        SECURITY_TYPE_MARKET_DATA)
#-----------------------------------------------------------------------------------------------------------------------
SYMBOL_STATUS_PRE_TRADING   = 'PRE_TRADING'
SYMBOL_STATUS_TRADING       = 'TRADING'
SYMBOL_STATUS_POST_TRADING  = 'POST_TRADING'
SYMBOL_STATUS_END_OF_DAY    = 'END_OF_DAY'
SYMBOL_STATUS_HALT          = 'HALT'
SYMBOL_STATUS_AUCTION_MATCH = 'AUCTION_MATCH'
SYMBOL_STATUS_BREAK         = 'BREAK        '
enum_symbol_status  =  (SYMBOL_STATUS_PRE_TRADING,SYMBOL_STATUS_TRADING,SYMBOL_STATUS_POST_TRADING, \
                        SYMBOL_STATUS_END_OF_DAY,SYMBOL_STATUS_HALT,SYMBOL_STATUS_AUCTION_MATCH,SYMBOL_STATUS_BREAK)
#-----------------------------------------------------------------------------------------------------------------------
enum_symbol_type  =  (SYMBOL_TYPE_SPOT)
#-----------------------------------------------------------------------------------------------------------------------
enum_time_in_force  =  (TIME_IN_FORCE_GTC,TIME_IN_FORCE_IOC,TIME_IN_FORCE_FOK)
#-----------------------------------------------------------------------------------------------------------------------
enum_websocket_depth = (WEBSOCKET_DEPTH_5,WEBSOCKET_DEPTH_10,WEBSOCKET_DEPTH_20)
