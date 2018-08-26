################################################################################
# Binance Pump configuration                                                   #
################################################################################

DATABASE_CONNECTION = {
    "host"     : "localhost",
    "port"     : "5432",
    "database" : "binancedb",
    "user"     : "binance",
    "password" : "123456"
}

STARTUP_ACTIONS = {
    "update_db_schema":  True,
}

# If symbols section not exists or empty all symbols will be loaded
# To select symbols for loading add list as shown above.
# Example:
#   "symbols":
#   [
#       { 
#           "symbol": "ETHBTC",
#           "aggTrades": True,
#           "trades": True,
#           "klines": True,
#           "kline_intervals": [ "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w","1M" ],
#           "miniTickers": True,
#           "tickers": True
#       },
#       { 
#           "symbol": "BTCUSD",
#           "aggTrades": True,
#           "trades": True,
#           "klines": True,
#           "kline_intervals": [ "1m", "1h", "1d", "1w", "1M" ],
#           "miniTickers": True,
#           "tickers": True
#       }
#   ]

DATA_TO_COLLECT = {
    "default": {
                 "aggTrades": True,
                 "trades": True,
                 "klines": True,
                 "kline_intervals": [ "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w","1M" ],
                 "miniTickers": True,
                 "tickers": True
               },
    "symbols": []
}
