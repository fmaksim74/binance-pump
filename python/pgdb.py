#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from binance.enums import *
from bncenums import *
import json
import psycopg2
from binance.client import Client

# REST tables
def rest_exchange_info_create_table_sql():
    r = 'CREATE TABLE IF NOT EXISTS "rest_exchangeInfo" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Name" VARCHAR(128) NOT NULL,' \
        '"_BaseUrl" VARCHAR(128) NOT NULL,' \
        '"_TimeZone" VARCHAR(128) NOT NULL,' \
        '"_RateLimits" JSONB,' \
        '"_ExchangeFilters" JSONB, ' \
        'CONSTRAINT "rest_exchangeInfo_pkey" PRIMARY KEY ("_rId")); COMMIT;'
    return r

def rest_exchange_info_insert_sql(data):
    r = 'INSERT INTO "rest_exchangeInfo" ' \
        '("_Name","_BaseUrl","_TimeZone","_RateLimits","_ExchangeFilters") ' \
        'VALUES (\'{name}\',\'{url}\',\'{tz}\',\'{rl}\',\'{ef}\'); COMMIT;'
    return r.format(name='Binance',url='http://api.binance.com',tz=data['timezone'],rl=json.dumps(data['rateLimits']),ef=json.dumps(data['exchangeFilters']))

def rest_exchange_info_update_sql(data):
    r = 'UPDATE "rest_exchangeInfo" SET "_RateLimits" = \'{rl}\', "_ExchangeFilters" = \'{ef}\' WHERE "_rId" = {i}; COMMIT;'
    return r.format(rl=json.dumps(data['rateLimits']),ef=json.dumps(data['exchangeFilters']),i=1)

def rest_exchange_info_update_sql(data):
    r = 'SELECT "_rId" FROM "ServerInfo" WHERE "_Name" = \'Binance\';'
    return r

def rest_exchange_info_drop_table_sql():
    r = 'DROP TABLE IF EXISTS "rest_exchangeInfo"; COMMIT;'
    return r

def rest_symbols_info_create_table_sql():
    r = 'CREATE TABLE IF NOT EXISTS "rest_symbolsInfo" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Symbol" VARCHAR(8) NOT NULL,' \
        '"_Status" symbol_status NOT NULL,' \
        '"_BaseAsset" VARCHAR(16) NOT NULL,' \
        '"_BasePrecision" SMALLINT DEFAULT 8,' \
        '"_QuoteAsset" VARCHAR(16) NOT NULL,' \
        '"_QuotePrecision" SMALLINT DEFAULT 8,' \
        '"_OrderTypes" JSONB,' \
        '"_IcebergAllowed" BOOLEAN,' \
        '"_Filters" JSONB,' \
        '"_Description" VARCHAR(128) DEFAULT NULL,' \
        'CONSTRAINT "rest_symbolsInfo_pkey" PRIMARY KEY ("_rId")); COMMIT;' \
        'CREATE UNIQUE INDEX IF NOT EXISTS "rest_symbolsInfo_lastsym_ix" ON "rest_symbolsInfo" ("_Symbol" ASC,"_rTime" ASC); COMMIT;'
    return r

def rest_symbols_info_insert_sql(data):
    r = 'INSERT INTO "rest_symbolsInfo" ' \
        '("_Symbol","_Status","_BaseAsset","_BasePrecision","_QuoteAsset","_QuotePrecision","_OrderTypes","_IcebergAllowed","_Filters","_Description") ' \
        'VALUES (\'{symbol}\',\'{status}\',\'{ba}\',{bp},\'{qa}\',{qp},\'{ot}\',\'{ia}\',\'{filters}\',\'{description}\'); COMMIT;'
    return r.format(symbol=data['symbol'],status=data['status'],ba=data['baseAsset'],bp=data['baseAssetPrecision'],qa=data['quoteAsset'],qp=data['quotePrecision'],
                    ot=json.dumps(data['orderTypes']),ia=data['icebergAllowed'],filters=json.dumps(data['filters']),description='')

def rest_symbols_info_update_sql(data):
    r = 'UPDATE "rest_symbolsInfo" ' \
        'SET "_Status"=\'{status}\',"_basePrecision"={bp},"_quotePrecision"={qp},"_orderTypes"={ot},"_icebergAllowed"=\'{ia}\',"_filters"=\'{filters}\',"_Description"=\'{description}\' ' \
        'WHERE "_Symbol"=\'{symbol}\';'
    return r.format(symbol=data['symbol'],status=data['status'],bp=data['baseAssetPrecision'],qp=data['quotePrecison'],
                    ot=data['orderTypes'],ia=data['icebergAllowed'],filters=data['filters'],description='')

def rest_symbols_info_drop_table_sql():
    r = 'DROP TABLE IF EXISTS "rest_symbolsInfo"; COMMIT;'
    return r

def rest_depth_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_depth{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_LastUpdateId" BIGINT,' \
        '"_Bids" JSONB,' \
        '"_Asks" JSONB,' \
        'CONSTRAINT "rest_depth{S}_pkey" PRIMARY KEY ("_rId")); COMMIT;' \
        'CREATE INDEX IF NOT EXISTS "rest_depth{S}_lupid" ON "rest_depth{S}" ("_lastUpdateId" ASC); COMMIT;'
    return r.format(S=symbol)

def rest_depth_insert_sql(params, data):
    r = 'INSERT INTO "rest_depth{S}" ("_LastUpdateId","_Bids","_Asks") ' \
        'VALUES ({i},\'{bids}\',\'{asks}\');'
    return r.format(S=params['symbol'],i=data['lastUpdateId'],bids=json.dumps(data['bids']),asks=json.dumps(data['asks']))

def rest_depth_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_depth{S}"; COMMIT;'
    return r.format(S=symbol)

def rest_trades_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_trades{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Id" BIGINT NOT NULL,' \
        '"_Price" NUMERIC NOT NULL,' \
        '"_Qty" NUMERIC NOT NULL,' \
        '"_Time" NUMERIC NOT NULL,' \
        '"_IsBuyerMaker" BOOLEAN NOT NULL,' \
        '"_IsBestMatch" BOOLEAN NOT NULL); COMMIT;'
    return r.format(S=symbol)

def rest_trades_insert_sql(params, data):
    r = 'INSERT INTO "rest_trades{S}" ("_Id","_Price","_Qty","_Time","_IsBuyerMaker","_IsBestMatch") VALUES ({I},{P},{Q},{T},{U},{E});'
    return r.format(S=params['symbol'],I=data['id'],P=data['price'],Q=data['qty'],T=data['time'],U=data['isBuyerMaker'],E=data['isBestMatch'])

def rest_trades_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_trades{S}"; COMMIT;'
    return r.format(S=symbol)

#aggTrades
def rest_agg_trades_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_aggTrades{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Id" BIGINT NOT NULL,' \
        '"_Price" NUMERIC NOT NULL,' \
        '"_Qty" NUMERIC NOT NULL,' \
        '"_FirstTradeId" BIGINT NOT NULL,' \
        '"_LastTradeId" BIGINT NOT NULL,' \
        '"_Time" NUMERIC NOT NULL,' \
        '"_IsBuyerMaker" BOOLEAN NOT NULL,' \
        '"_IsBestMatch" BOOLEAN NOT NULL); COMMIT;'
    return r.format(S=symbol)

def rest_agg_trades_insert_sql(params, data):
    r = 'INSERT INTO "rest_aggTrades{S}" ("_Id","_Price","_Qty","_FirstTradeId","_LastTradeId","_Time","_IsBuyerMaker","_IsBestMatch") VALUES ({I},{P},{Q},{F},{L},{T},{U},{E});'
    return r.format(S=params['symbol'],I=data['a'],P=data['p'],Q=data['q'],F=data['f'],L=data['l'],T=data['T'],U=data['m'],E=data['M'])

def rest_agg_trades_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_aggTrades{S}"; COMMIT;'
    return r.format(S=symbol)


def rest_kline_create_table_sql(symbol, interval):
    r = 'CREATE TABLE IF NOT EXISTS "rest_kline{S}_{I}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_OpenTime" BIGINT,' \
        '"_Open" NUMERIC,' \
        '"_High" NUMERIC,' \
        '"_Low"  NUMERIC,' \
        '"_Close" NUMERIC,' \
        '"_Volume" NUMERIC,' \
        '"_CloseTime" BIGINT,' \
        '"_QuoteAssetVolume" NUMERIC,' \
        '"_NumerOfTrades" BIGINT,' \
        '"_TakerByBaseAssetVolume" NUMERIC,' \
        '"_TakerBuyQuoteAssetVolume" NUMERIC,' \
        '"_Ignore" NUMERIC); COMMIT;' \
        'CREATE UNIQUE INDEX IF NOT EXISTS "rest_kline{S}_{I}_OT_IX" ON "rest_kline{S}_{I}" ("_OpenTime" ASC); COMMIT;' \
        'CREATE INDEX IF NOT EXISTS "rest_kline{S}_{I}_OCT_IX" ON "rest_kline{S}_{I}" ("_OpenTime" ASC, "_CloseTime" ASC); COMMIT;'
    return r.format(S=symbol,I=interval)

def rest_kline_insert_sql(params, data):
    r = 'INSERT INTO "rest_kline{S}_{I}" ' \
        '("_OpenTime","_Open","_High","_Low","_Close","_Volume","_CloseTime","_QuoteAssetVolume",' \
        '"_NumerOfTrades","_TakerByBaseAssetVolume","_TakerBuyQuoteAssetVolume","_Ignore")\n' \
        'VALUES ({OT},{O},{H},{L},{C},{V},{CT},{QAV},{NoT},{TBBA},{TBQA},{IG}) ON CONFLICT DO NOTHING;'
    r = r.format(S=params['symbol'],I=params['interval'],
                 OT=data[0],O=data[1],H=data[2],L=data[3],C=data[4],V=data[5],
                 CT=data[6],QAV=data[7],NoT=data[8],TBBA=data[9],TBQA=data[10],IG=data[11])
    print(r)
    return r

def rest_kline_drop_table_sql(symbol, interval):
    r = 'DROP TABLE IF EXISTS "rest_kline{S}_{I}";COMMIT;'
    return r.format(S=symbol,I=interval)

def rest_24hr_ticker_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_24hr_ticker{S}" (' \
        '    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '    "_PriceChange" NUMERIC,' \
        '    "_PriceChangePercent" NUMERIC,' \
        '    "_WeightedAvgPrice" NUMERIC,' \
        '    "_PrevClosePrice" NUMERIC,' \
        '    "_LastPrice" NUMERIC,' \
        '    "_LastQty" NUMERIC,' \
        '    "_BidPrice" NUMERIC,' \
        '    "_AskPrice" NUMERIC,' \
        '    "_OpenPrice" NUMERIC,' \
        '    "_HighPrice" NUMERIC,' \
        '    "_LowPrice" NUMERIC,' \
        '    "_Volume" NUMERIC,' \
        '    "_QuoteVolume" NUMERIC,' \
        '    "_OpenTime" BIGINT,' \
        '    "_CloseTime" BIGINT,' \
        '    "_FirstId" BIGINT,' \
        '    "_LastId" BIGINT,' \
        '    "_Count" BIGINT); COMMIT;'
    return r.format(S=symbol)

def rest_24hr_ticker_insert_sql(params, data):
    r = 'INSERT INTO "rest_24hr_ticker{S}" ' \
        '("_PriceChange","_PriceChangePercent","_WeightedAvgPrice","_PrevClosePrice","_LastPrice","_LastQty","_BidPrice","_AskPrice",' \
        '"_OpenPrice","_HighPrice","_LowPrice","_Volume","_QuoteVolume","_OpenTime","_CloseTime","_FirstId","_LastId","_Count") ' \
        'VALUES ({p1},{p2},{p3},{p4},{p5},{p6},{p7},{p8},{p9},{p10},{p11},{p12},{p13},{p14},{p15},{p16},{p17},{p18}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['symbol'],
                    p1=data['priceChange'],p2=data['priceChangePercent'],p3=data['weightedAvgPrice'],p4=data['prevClosePrice'],p5=data['lastPrice'],
                    p6=data['lastQty'],p7=data['bidPrice'],p8=data['askPrice'],p9=data['openPrice'],p10=data['highPrice'],p11=data['lowPrice'],
                    p12=data['volume'],p13=data['quoteVolume'],p14=data['openTime'],p15=data['closeTime'],p16=data['firstId'],p17=data['lastId'],
                    p18=data['count'])

def rest_24hr_ticker_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_24hr_ticker{S}"; COMMIT;'
    return r.format(S=symbol)

def rest_price_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_price{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Price" NUMERIC NOT NULL); COMMIT;'
    return r.format(S=symbol)

def rest_price_insert_sql(params, data):
    r = 'INSERT INTO "rest_price{S}" ("_Price") VALUES ({P});'
    return r.format(S=data['symbol'],P=data['price'])

def rest_price_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_price{S}"; COMMIT;'
    return r.format(S=symbol)

def rest_book_ticker_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "rest_price{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_Price" NUMERIC NOT NULL); COMMIT;'
    return r.format(S=symbol)

def rest_book_ticker_insert_sql(params, data):
    r = 'INSERT INTO "rest_bookTicker{S}" ("_bidPrice","_bidQty","_askPrice","_askQty") VALUES ({bp},{bq},{ap},{aq});'
    return r.format(S=data['symbol'],bp=data['bidPrice'],bq=data['bidQty'],ap=data['askPrice'],aq=data['askQty'])

def rest_book_ticker_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "rest_price{S}"; COMMIT;'
    return r.format(S=symbol)

# WSS tables
def wss_aggTrade_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "wss_aggTrade{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_AggregateTradeID" BIGINT,' \
        '"_Price" NUMERIC,' \
        '"_Quantity" NUMERIC,' \
        '"_FirstTradeID" BIGINT,' \
        '"_LastTradeID" BIGINT,' \
        '"_TradeTime" BIGINT,' \
        '"_IsTheBuyerTheMarketMaker" BOOLEAN,' \
        '"_Ignore" BOOLEAN,' \
        'CONSTRAINT "wss_aggTrades_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol)

def wss_aggTrade_insert_sql(data):
    r = 'INSERT INTO "wss_aggTrade{S}" ' \
        '("_EventTime","_AggregateTradeID","_Price","_Quantity","_FirstTradeID","_LastTradeID","_TradeTime","_IsTheBuyerTheMarketMaker","_Ignore") ' \
        'VALUES ({E},{a},{p},{q},{f},{l},{T},{m},{M}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],a=data['a'],p=data['p'],q=data['q'],f=data['f'],l=data['l'],T=data['T'],m=data['m'],M=data['M'])

def wss_aggTrade_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "wss_aggTrade{S}"; COMMIT;'
    return r.format(S=symbol)

def wss_trade_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "wss_trade{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_TradeID" BIGINT,' \
        '"_Price" NUMERIC,' \
        '"_Quantity" NUMERIC,' \
        '"_BuyerOrderID" BIGINT,' \
        '"_SellerOrderID" BIGINT,' \
        '"_TradeTime" BIGINT,' \
        '"_IsTheBuyerTheMarketMaker" BOOLEAN,' \
        '"_Ignore" BOOLEAN,' \
        'CONSTRAINT "wss_trades{S}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol)

def wss_trade_insert_sql(data):
    r = 'INSERT INTO "wss_trade{S}" ' \
        '("_EventTime","_TradeID","_Price","_Quantity","_BuyerOrderID","_SellerOrderID","_TradeTime","_IsTheBuyerTheMarketMaker","_Ignore") ' \
        'VALUES({E},{t},{p},{q},{b},{a},{T},{m},{M}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],t=data['t'],p=data['p'],q=data['q'],b=data['b'],a=data['a'],T=data['T'],m=data['m'],M=data['M'])

def wss_trade_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "wss_trade{S}"; COMMIT;'
    return r.format(S=symbol)

def wss_kline_create_table_sql(symbol, interval):
    r = 'CREATE TABLE IF NOT EXISTS "wss_kline{S}_{I}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_StartTime" BIGINT,' \
        '"_CloseTime" BIGINT,' \
        '"_FirstTradeId" BIGINT,' \
        '"_LastTradeId" BIGINT,' \
        '"_OpenPrice" NUMERIC,' \
        '"_ClosePrice" NUMERIC,' \
        '"_HighPrice" NUMERIC,' \
        '"_LowPrice" NUMERIC,' \
        '"_BaseAssetVolume" NUMERIC,' \
        '"_NumberOfTrades" BIGINT,' \
        '"_KlineClosed" BOOLEAN,' \
        '"_QuoteAssetVolume" NUMERIC,' \
        '"_TakerBuyBaseAssetVolume" NUMERIC,' \
        '"_TaherBuyQuoteAssetVolume" NUMERIC,' \
        '"_IgnoreField" BIGINT,' \
        'CONSTRAINT "wss_klines{S}_{I}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol,I=interval)

def wss_kline_insert_sql(data):
    r = 'INSERT INTO "wss_kline{S}_{I}" ' \
        '("_EventTime","_StartTime","_CloseTime","_FirstTradeId","_LastTradeId","_OpenPrice","_ClosePrice","_HighPrice","_LowPrice",' \
        '"_BaseAssetVolume","_NumberOfTrades","_KlineClosed","_QuoteAssetVolume","_TakerBuyBaseAssetVolume","_TaherBuyQuoteAssetVolume","_IgnoreField") ' \
        'VALUES ({E},{t},{T},{f},{L},{o},{c},{h},{l},{v},{n},{x},{q},{V},{Q},{B}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],I=data['k']['i'],t=data['k']['t'],T=data['k']['T'],f=data['k']['f'],L=data['k']['L'],o=data['k']['o'],
                    c=data['k']['c'],h=data['k']['h'],l=data['k']['l'],v=data['k']['v'],n=data['k']['n'],x=data['k']['x'],q=data['k']['q'],V=data['k']['V'],Q=data['k']['Q'],B=data['k']['B'])

def wss_kline_drop_table_sql(symbol, interval):
    r = 'DROP TABLE IF EXISTS "wss_kline{S}_{I}"; COMMIT;'
    return r.format(S=symbol,I=interval)

def wss_24hrMiniTicker_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "wss_24hrMiniTicker{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_CurrentDayClosePrice" NUMERIC,' \
        '"_OpenPrice" NUMERIC,' \
        '"_HighPrice" NUMERIC,' \
        '"_LowPrice" NUMERIC,' \
        '"_TotalTradedBaseAssetVolume" NUMERIC,' \
        '"_TotalTradedQuoteAssetVolume" NUMERIC,' \
        'CONSTRAINT "wss_24hrMiniTicker{S}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol)

def wss_24hrMiniTicker_insert_sql(data):
    r = 'INSERT INTO "wss_24hrMiniTicker{S}" ' \
        '("_EventTime","_CurrentDayClosePrice","_OpenPrice","_HighPrice","_LowPrice","_TotalTradedBaseAssetVolume","_TotalTradedQuoteAssetVolume") ' \
        'VALUES ({E},{c},{o},{h},{l},{v},{q}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],c=data['c'],o=data['o'],h=data['h'],l=data['l'],v=data['v'],q=data['q'])

def wss_24hrMiniTicker_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "wss_24hrMiniTicker{S}"; COMMIT;'
    return r.format(S=symbol)

def wss_24hrTicker_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "wss_24hrTicker{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_PriceChange" NUMERIC,' \
        '"_PriceChangePercent" NUMERIC,' \
        '"_WeightedAveragePrice" NUMERIC,' \
        '"_PreviousDaysClosePrice" NUMERIC,' \
        '"_CurrentDaysClosePrice" NUMERIC,' \
        '"_CloseTradesQuantity" NUMERIC,' \
        '"_BestBidPrice" NUMERIC,' \
        '"_BestBidQuantity" NUMERIC,' \
        '"_BestAskPrice" NUMERIC,' \
        '"_BestAskQuantity" NUMERIC,' \
        '"_OpenPrice" NUMERIC,' \
        '"_HighPrice" NUMERIC,' \
        '"_LowPrice" NUMERIC,' \
        '"_TotalTradedBaseAssetVolume" NUMERIC,' \
        '"_TotalTradedQuoteAssetVolume" NUMERIC,' \
        '"_StatisticsOpenTime" BIGINT,' \
        '"_StatisticsCloseTime" BIGINT,' \
        '"_FirstTradeID" BIGINT,' \
        '"_LastTradeId" BIGINT,' \
        '"_TotalNumberOfTrades",' \
        'CONSTRAINT "wss_24hrTicker{S}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol)

def wss_24hrTicker_insert_sql(data):
    r = 'INSERT INTO "wss_24hrTicker{S}" ' \
        '("_EventTime","_PriceChange","_PriceChangePercent","_WeightedAveragePrice","_PreviousDaysClosePrice","_CurrentDaysClosePrice","_CloseTradesQuantity",' \
        '"_BestBidPrice","_BestBidQuantity","_BestAskPrice"."_BestAskQuantity","_OpenPrice","_HighPrice","_LowPrice","_TotalTradedBaseAssetVolume",' \
        '"_TotalTradedQuoteAssetVolume","_StatisticsOpenTime","_StatisticsCloseTime","_FirstTradeID","_LastTradeId","_TotalNumberOfTrades") ' \
        'VALUES ({E},{p},{P},{w},{x},{c},{Q},{b},{B},{a},{A},{o},{h},{l},{v},{q},{O},{C},{F},{L},{n}) ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],p=data['p'],P=data['P'],w=data['w'],x=data['x'],c=data['c'],Q=data['Q'],b=data['b'],B=data['B'],a=data['a'],
                    A=data['A'],o=data['o'],h=data['h'],l=data['l'],v=data['v'],q=data['q'],O=data['O'],C=data['C'],F=data['F'],L=data['L'],n=data['n'])

def wss_24hrTicker_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "wss_24hrTicker{S}";'
    return r.format(S=symbol)

def wss_depth_level_create_table_sql(symbol, level):
    r = 'CREATE TABLE IF NOT EXISTS "wss_depth{S}{L}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_LastUpdateId" BIGINT,' \
        '"_Bids" JSONB,' \
        '"_Asks" JSONB,' \
        'CONSTRAINT "wss_depth{S}{L}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol,L=str(level))

def wss_depth_level_insert_sql(params, data):
    r = 'INSERT INTO "wss_depth{S}{L}" ("_LastUpdateId","_Bids","_Asks") VALUES ({lastUpdateId},\'{bids}\',\'{asks}\') ON CONFLICT DO NOTHING;'
    return r.format(S=params['symbol'],L=str(params['level']),lastUpdateId=data['lastUpdateId'],bids=json.dumps(data['bids']),asks=json.dumps(data['asks']))

def wss_depth_level_drop_table_sql(symbol, level):
    r = 'DROP TABLE IF EXISTS "wss_depth{S}{L}"; COMMIT;'
    return r.format(S=symbol,L=str(level))

def wss_depth_create_table_sql(symbol):
    r = 'CREATE TABLE IF NOT EXISTS "wss_depth{S}" (' \
        '"_rId" BIGINT GENERATED ALWAYS AS IDENTITY,' \
        '"_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
        '"_EventTime" BIGINT,' \
        '"_FirstUpdateID" BIGINT,' \
        '"_FinalUpdateID" BIGINT,' \
        '"_Bids" JSONB,' \
        '"_Asks" JSONB,'
        'CONSTRAINT "wss_depth{S}_EventTime_Unique" UNIQUE("_EventTime")); COMMIT;'
    return r.format(S=symbol)

def wss_depth_insert_sql(data):
    r = 'INSERT INTO "wss_depth{S}" ("_EventTime","_FirstUpdateID","_FinalUpdateID","_Bids","_Asks") ' \
        'VALUES ({E},{U},{u},\'{b}\',\'{a}\') ON CONFLICT DO NOTHING;'
    return r.format(S=data['s'],E=data['E'],U=data['U'],u=data['u'],b=json.dumps(data['b']),a=json.dumps(data['a']))

def wss_depth_drop_table_sql(symbol):
    r = 'DROP TABLE IF EXISTS "wss_depth{S}"; COMMIT;'
    return r.format(S=symbol)

def common_schema_create_sql():
    return '\n'.join((rest_exchange_info_create_table_sql(), rest_symbols_info_create_table_sql()))

def common_schema_save_data_sql(data):
    return rest_exchange_info_insert_sql(data) + '\n' + '\n'.join([rest_symbols_info_insert_sql(symbol) for symbol in data['symbols']])

def common_schema_drop_sql():
    return '\n'.join((rest_exchange_info_drop_table_sql(), rest_symbols_info_drop_table_sql()))

def symbol_schema_create_sql(symbol):
    # rest
    r = '\n'+rest_depth_create_table_sql(symbol)
    r += '\n'+rest_trades_create_table_sql(symbol)
    r += '\n'+rest_agg_trades_create_table_sql(symbol)
    r += '\n'+'\n'.join([rest_kline_create_table_sql(symbol, interval) for interval in enum_kline_intervals])
    r += '\n'+rest_24hr_ticker_create_table_sql(symbol)
    r += '\n'+rest_price_create_table_sql(symbol)
    r += '\n'+rest_book_ticker_create_table_sql(symbol)
    # wss
    r += '\n'+wss_aggTrade_create_table_sql(symbol)
    r += '\n'+wss_trade_create_table_sql(symbol)
    r += '\n'+'\n'.join([wss_kline_create_table_sql(symbol, interval) for interval in enum_kline_intervals])
    r += '\n'+wss_24hrMiniTicker_create_table_sql(symbol)
    r += '\n'+wss_24hrTicker_create_table_sql(symbol)
    r += '\n'+'\n'.join([wss_depth_level_create_table_sql(symbol, level) for level in enum_websocket_depth])
    r += '\n'+wss_depth_create_table_sql(symbol)
    return r

def symbol_schema_drop_sql(symbol):
    # rest
    r = '\n'+rest_depth_drop_table_sql(symbol)
    r += '\n'+rest_trades_drop_table_sql(symbol)
    r += '\n'+rest_agg_trades_drop_table_sql(symbol)
    r += '\n'+'\n'.join([rest_kline_drop_table_sql(symbol, interval) for interval in enum_kline_intervals])
    r += '\n'+rest_24hr_ticker_drop_table_sql(symbol)
    r += '\n'+rest_price_drop_table_sql(symbol)
    r += '\n'+rest_book_ticker_drop_table_sql(symbol)
    # wss
    r += '\n'+wss_aggTrade_drop_table_sql(symbol)
    r += '\n'+wss_trade_drop_table_sql(symbol)
    r += '\n'+'\n'.join([wss_kline_drop_table_sql(symbol, interval) for interval in enum_kline_intervals])
    r += '\n'+wss_24hrMiniTicker_drop_table_sql(symbol)
    r += '\n'+wss_24hrTicker_drop_table_sql(symbol)
    r += '\n'+'\n'.join([wss_depth_level_drop_table_sql(symbol, level) for level in enum_websocket_depth])
    r += '\n'+wss_depth_drop_table_sql(symbol)
    return r

class BinanceDB(object):

    __db_connection = None
    __lastUpdateId = 0

    def __init__(self):
        self.__cursor = None
        self.__alive = False
        self.Connect()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__db_connection is not None:
            self.__db_connection.close()

    def Connect(self):
        if type(self).__db_connection is None:
            type(self).__db_connection = psycopg2.connect(dbname='binancedb', user='binance', password='123456', host='localhost')
            if (not type(self).__db_connection.closed) and (self.__cursor is None):
                self.__cursor = type(self).__db_connection.cursor()
                self.__alive = True

    def CreateCommonSchema(self, data):  # data should be the exchangeInfo
        if (self.__alive) and (data is not None):
            self.__cursor.execute(common_schema_create_sql())
            self.__cursor.execute(common_schema_save_data_sql(data))
            
    def DropCommonSchema(self):
        if (self.__alive):
            self.__cursor.execute(common_schema_drop_sql())

    def UpdateCommonSchema(self, data, drop=False): # data - exchangeInfo
        if (self.__alive):
            if drop: self.DropCommonSchema()
            self.CreateCommonSchema(data)
    
    def CreateSymbolSchema(self, data):
        if (self.__alive) and (data is not None):
            if isinstance(data, str):  # if data is single string with symbol name
                self.__cursor.execute(symbol_schema_create_sql(symbol))
            if isinstance(data, list): 
                for symbol in data: 
                    if isinstance(symbol,str): # if data is string list with symbol names
                        self.__cursor.execute(symbol_schema_create_sql(symbol))
                    if isinstance(symbol,dict): # if data is 'symbol' nodes list from exchangeInfo
                        self.__cursor.execute(symbol_schema_create_sql(symbol['symbol']))
            if isinstance(data, dict): # if data is exchangeInfo
                if 'symbols' in data:
                    for symbol in data['symbols']: # if data is whole exchangeInfo
                        self.__cursor.execute(symbol_schema_create_sql(symbol['symbol']))
                if 'symbol' in data: # if data is symbol node from exchnageInfo only
                    self.__cursor.execute(symbol_schema_create_sql(data['symbol']))
                

    def DropSymbolSchema(self, data):
        if (self.__alive) and (data is not None):
            if isinstance(data, str):  # if data is single string with symbol name
                self.__cursor.execute(symbol_schema_drop_sql(symbol))
            if isinstance(data, list): 
                for symbol in data: 
                    if isinstance(symbol,str): # if data is string list with symbol names
                        self.__cursor.execute(symbol_schema_drop_sql(symbol))
                    if isinstance(symbol,dict): # if data is 'symbol' nodes list from exchangeInfo
                        self.__cursor.execute(symbol_schema_drop_sql(symbol['symbol']))
            if isinstance(data, dict): # if data is exchangeInfo
                if 'symbols' in data:
                    for symbol in data['symbols']: # if data is whole exchangeInfo
                        self.__cursor.execute(symbol_schema_drop_sql(symbol['symbol']))
                if 'symbol' in data: # if data is symbol node from exchnageInfo only
                    self.__cursor.execute(symbol_schema_drop_sql(data['symbol']))

    def UpdateSymbolSchema(self, data, drop=False):
        if (self.__alive):
            if drop:
                self.DropSymbolSchema(data)
            self.CreateSymbolSchema(data)

    def SaveSymbolInfo(self, data):   
            if isinstance(data, dict):
                if 'symbols' in data:  # data is exchangeInfo
                    for symbol in data['symbols']:
                        self.__cursor.execute(rest_symbols_info_insert_sql(symbol))
                if 'symbol' in data: # data is symbol node
                    self.__cursor.execute(rest_symbols_info_insert_sql(data))
            if isinstance(data, list): # data is symbols list
                for symbol in data: 
                    if isinstance(symbol,dict) and ('symbol' in data): # data is 'symbol' node
                        self.__cursor.execute(rest_symbols_info_insert_sql(symbol))

    def restSaveDepth(self, params, data): # params - request params, data - request result
        if (self.__alive):
            self.__cursor.execute(rest_depth_insert_sql(params, data))
    
    def restSaveTrades(self, params, data):
        if (self.__alive):
            if isinstance(data, dict): # single trade record
                self.__cursor.execute(rest_trades_insert_sql(params, data))
            if isinstance(data, list): # list of trades
                for d in data:
                    self.__cursor.execute(rest_trades_insert_sql(params, d))

    def restSaveAggTrades(self, params, data):
        if (self.__alive):
            if isinstance(data, dict): # single agg trade record
                self.__cursor.execute(rest_agg_trades_insert_sql(params, data))
            if isinstance(data, list): # list of agg trades
                for d in data:
                    self.__cursor.execute(rest_agg_trades_insert_sql(params, d))

    def restSaveKLine(self, params, data):
        if (self.__alive):
            if (isinstance(data, list)) and (len(data) > 0) and (not isinstance(data[0], list)): # data is single kline
                self.__cursor.execute(rest_kline_insert_sql(params, data))
            if (isinstance(data, list)) and (len(data) > 0) and (isinstance(data[0], list)): # data is list of klines
                for d in data:
                    self.__cursor.execute(rest_kline_insert_sql(params, d))

    def restSave24hrTicker(self, params, data):
        if (self.__alive):
            if isinstance(data, dict): # data is single ticker 
                self.__cursor.execute(rest_24hr_ticker_insert_sql(params, data))
            if isinstance(data, list): # data is list of tickers
                for d in data:
                    self.__cursor.execute(rest_24hr_ticker_insert_sql(params, d))

    def restSavePrice(self, params, data):
        if (self.__alive):
            if isinstance(data, dict): # data is single ticker 
                self.__cursor.execute(rest_price_insert_sql(params, data))
            if isinstance(data, list): # data is list of tickers
                for d in data:
                    self.__cursor.execute(rest_price_insert_sql(params, d))

    def restSaveBookTicker(self, params, data):
        if (self.__alive):
            if isinstance(data, dict): # data is single ticker 
                self.__cursor.execute(rest_book_ticker_insert_sql(params, data))
            if isinstance(data, list): # data is list of tickers
                for d in data:
                    self.__cursor.execute(rest_book_ticker_insert_sql(params, d))

    def wssSaveAggTrade(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_aggTrade_insert_sql(data))

    def wssSaveTrade(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_trade_insert_sql(data))

    def wssSaveKLine(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_kline_insert_sql(data))

    def wssSave24hrMiniTicker(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_24hrMiniTicker_insert_sql(data))

    def wssSave24hrTicker(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_24hrTicker_insert_sql(data))

    def wssSaveArr(self, data):
        if (self.__alive) and (data is not None):
            stream = data['stream'].split(sep='@')[0]
            if stream == '!miniTicker':
                self.wssSave24hrMiniTicker(data['data'])
            if stream == '!ticker':
                self.wssSave24hrTicker(data['data'])

    def wssSaveDepthLevel(self, symbol, level, data):
        if (self.__alive):
            self.__cursor.execute(wss_depth_level_insert_sql(data))

    def wssSaveDepthDiff(self, data):
        if (self.__alive):
            self.__cursor.execute(wss_depth_insert_sql(data))

    def wssSaveDepth(self, data):
        pass

    def wssSaveMsg(self, data):
        if (self.__alive) and (data is not None):
            # Split stream name to symbol name and stream name
            stream = data['stream'].split(sep='@')[1]
            if stream[1][:len('aggTrade')] == 'aggTrade':
                self.wssSaveAggTrade(data['data'])
            if stream[1][:len('trade')] == 'trade':
                self.wssSaveTrade(data['data'])
            if stream[1][:len('kline')] == 'kline':
                self.wssSaveKLine(data['data'])
            if stream[1] == 'arr':
                self.SaveArr(data)
            if stream[1][:len('depth')] == 'depth':
                self.wssSaveDepth(data)
            self.Commit()

    def Commit(self):
        if (self.__alive):
            self.__cursor.connection.commit()


def main():
    bnc = Client('','')
    bdb = BinanceDB()
    exch = bnc.get_exchange_info()
    bdb.UpdateCommonScheme(exch, True)
    bdb.UpdateSymbolScheme(exch, True)

if __name__ == '__main__':
#   main()
    exit()
