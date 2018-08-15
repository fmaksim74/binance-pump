-- #####################################################################################################################
------------------------------------------------------------------------------------------------------------------------
-- Create custom data types
------------------------------------------------------------------------------------------------------------------------
DROP TYPE IF EXISTS security_type; COMMIT;
CREATE TYPE security_type AS ENUM ('NONE','TRADE','USER_DATA','USER_STREAM','MARKET_DATA');

DROP TYPE IF EXISTS symbol_status; COMMIT;
CREATE TYPE symbol_status AS ENUM ('PRE_TRADING','TRADING','POST_TRADING','END_OF_DAY','HALT','AUCTION_MATCH','BREAK');

DROP TYPE IF EXISTS symbol_type; COMMIT;
CREATE TYPE symbol_type AS ENUM ('SPOT');

DROP TYPE IF EXISTS order_status; COMMIT;
CREATE TYPE order_status AS ENUM ('NEW','PARTIALLY_FILLED','FILLED','CANCELED','PENDING_CANCEL','REJECTED','EXPIRED');

DROP TYPE IF EXISTS order_type; COMMIT;
CREATE TYPE order_type AS ENUM 
    ('LIMIT','MARKET','STOP_LOSS','STOP_LOSS_LIMIT','TAKE_PROFIT','TAKE_PROFIT_LIMIT','LIMIT_MAKER');

DROP TYPE IF EXISTS order_side; COMMIT;
CREATE TYPE order_side AS ENUM ('BUY','SELL');

DROP TYPE IF EXISTS time_in_force; COMMIT;
CREATE TYPE time_in_force AS ENUM ('GTC','IOC','FOK');

DROP TYPE IF EXISTS kline_intervals; COMMIT;
CREATE TYPE kline_intervals AS ENUM
    ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w','1M');

DROP TYPE IF EXISTS rate_limiter; COMMIT;
CREATE TYPE rate_limiter AS ENUM ('REQUESTS', 'ORDERS');

DROP TYPE IF EXISTS rate_limit_intervals; COMMIT;
CREATE TYPE rate_limit_intervals AS ENUM ('SECOND', 'MINUTE', 'DAY');
/*
------------------------------------------------------------------------------------------------------------------------
-- Create base tables
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
-- Templates for REST data
------------------------------------------------------------------------------------------------------------------------
-- ExchangeInfo
DROP TABLE IF EXISTS "rest_exchangeInfo"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_exchangeInfo" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_Name" VARCHAR(128) NOT NULL,
    "_BaseUrl" VARCHAR(128) NOT NULL,
    "_TimeZone" VARCHAR(128) NOT NULL,
    "_RateLimits" JSONB,
    "_ExchangeFilters" JSONB,
    CONSTRAINT "rest_exchangeInfo_pkey" PRIMARY KEY ("_Id")
);
-- Symbols from ExchangeInfo
DROP TABLE IF EXISTS "rest_symbolsInfo"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_symbolsInfo" (
    "_Id" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_Symbol" CHAR(8) NOT NULL,
    "_Status" BIGINT NOT NULL,
    "_baseAsset" BIGINT NOT NULL,
    "_basePrecision" SMALLINT DEFAULT 8,
    "_quoteAsset" BIGINT NOT NULL,
    "_quotePrecision" SMALLINT DEFAULT 8,
    "_orderTypes" JSONB,
    "_icebergAllowed" BOOLEAN,
    "_filters" JSONB,
    "_Description" VARCHAR(128) DEFAULT NULL,
    CONSTRAINT "rest_symbolsInfo_pkey" PRIMARY KEY ("_Id")
);
CREATE INDEX IF NOT EXISTS "rest_symbolsInfo_lastsym_ix" ON "rest_symbolsInfo" ("_Symbol" ASC,"_Time" ASC); COMMIT;
INSERT INTO "rest_symbolsInfo"
    ("_Symbol","_Status","_baseAsset","_basePrecision","_quoteAsset","_quotePrecision",
     "_orderTypes","_icebergAllowed","_filters","_Description")
VALUES 
    ({},{},{},{},{},{},{},{},{},{});
UPDATE "rest_symbolsInfo"
    SET "_Status"={},"_basePrecision"={},"_quotePrecision"={},
        "_orderTypes"={},"_icebergAllowed"={},"_filters"={},
        "_Description"={}
WHERE "_Symbol"={};
------------------------------------------------------------------------------------------------------------------------
-- Templates for REST data
------------------------------------------------------------------------------------------------------------------------
-- Order book (depth)
DROP TABLE IF EXISTS "rest_depth{S}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_depth{S}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_lastUpdateId" BIGINT,
    "_bids" JSONB,
    "_asks" JSONB,
    CONSTRAINT "rest_depth{S}_pkey" PRIMARY KEY ("_Id")
); COMMIT;
CREATE INDEX IF NOT EXISTS "rest_depth{S}_pkey" ON "rest_depth{S}_pkey" ("_lastUpdateId" ASC); COMMIT;
INSERT INTO "rest_depth{S}" ("_lastUpdateId","_bids","_asks") VALUES ({},{},{});
-- Recent trades list (trades)
DROP TABLE IF EXISTS "rest_trades{S}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_trades{S}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_Id" BIGINT NOT NULL,
    "_Price" NUMERIC NOT NULL,
    "_Qty" NUMERIC NOT NULL,
    "_Time" NUMERIC NOT NULL,
    "_IsBuyerMaker" BOOLEAN NOT NULL,
    "_IsBestMatch" BOOLEAN NOT NULL
); COMMIT;
INSERT INTO "rest_trades{S}" ("_Id","_Price","_Qty","_Time","_IsBuyerMaker","_IsBestMatch") VALUES ({},{},{},{},{},{});
-- Kline/Candlestik
DROP TABLE IF EXISTS "rest_kline{S}_{I}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_kline{S}_{I}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_OpenTime" BIGINT,
    "_Open" NUMERIC,
    "_High" NUMERIC,
    "_Low"  NUMERIC,
    "_Close" NUMERIC,
    "_Volume" NUMERIC,
    "_CloseTime" BIGINT,
    "_QuoteAssetVolume" NUMERIC,
    "_NumerOfTrades" BIGINT,
    "_TakerByBaseAssetVolume" NUMERIC,
    "_TakerBuyQuoteAssetVolume" NUMERIC,
    "Ignore" NUMERIC
); COMMIT;
CREATE UNIQUE INDEX IF NOT EXISTS "rest_kline{S}_{I}_OCT_IX" ON "rest_kline{S}_{I}" ("_OpenTime" ASC); COMMIT;
CREATE INDEX IF NOT EXISTS "rest_kline{S}_{I}_OCT_IX" ON "rest_kline{S}_{I}" ("_OpenTime" ASC, "_CloseTime" ASC); COMMIT;
INSERT INTO "rest_kline{S}_{I}"
    ("_OpenTime","_Open","_High","_Low","_Close","_Volume","_CloseTime","_QuoteAssetVolume",
     "_NumerOfTrades","_TakerByBaseAssetVolume","_TakerBuyQuoteAssetVolume","Ignore")
VALUES ({},{},{},{},{},{},{},{},{},{},{},{}) ON CONFLICT DO NOTHING;
-- 24hr ticker
DROP TABLE IF EXISTS "rest_24hr_ticker{S}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_24hr_ticker{S}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_priceChange" NUMERIC,
    "_priceChangePercent" NUMERIC,
    "_weightedAvgPrice" NUMERIC,
    "_prevClosePrice" NUMERIC,
    "_lastPrice" NUMERIC,
    "_lastQty" NUMERIC,
    "_bidPrice" NUMERIC,
    "_askPrice" NUMERIC,
    "_openPrice" NUMERIC,
    "_highPrice" NUMERIC,
    "_lowPrice" NUMERIC,
    "_volume" NUMERIC,
    "_quoteVolume" NUMERIC,
    "_openTime" BIGINT,
    "_closeTime" BIGINT,
    "_firstId" BIGINT,
    "_lastId" BIGINT,
    "_count" BIGINT
);
CREATE UNIQUE INDEX IF NOT EXISTS "rest_24hr_ticker{S}_OCT_IX" ON "rest_24hr_ticker{S}" ("_openTime" ASC, "_closeTime" ASC); COMMIT;
INSERT INTO "rest_24hr_ticker{S}"
    ("_priceChange","_priceChangePercent","_weightedAvgPrice","_prevClosePrice","_lastPrice","_lastQty","_bidPrice","_askPrice",
     "_openPrice","_highPrice","_lowPrice","_volume","_quoteVolume","_openTime","_closeTime","_firstId","_lastId","_count")
VALUES
    ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}) ON CONFLICT DO NOTHING;
-- Price
DROP TABLE IF EXISTS "rest_price{S}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_price{S}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_Price" NUMERIC NOT NULL
); COMMIT;
INSERT INTO "rest_price{S}" ("_Price") VALUES ({});
-- bookTicker
DROP TABLE IF EXISTS "rest_bookTicker{S}"; COMMIT;
CREATE TABLE IF NOT EXISTS "rest_bookTiker{}" (
    "_rId" BIGINT GENERATED ALWAYS AS IDENTITY,
    "_rTime" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "_bidPrice"  NUMERIC(8) NOT NULL,
    "_bidQty"  NUMERIC(8) NOT NULL,
    "_askPrice"  NUMERIC(8) NOT NULL,
    "_askQty"  NUMERIC(8) NOT NULL
); COMMIT;
INSERT INTO "rest_bookTicker{S}" ("_bidPrice","_bidQty","_askPrice","_askQty") VALUES ({bp},{bq},{ap},{aq});
------------------------------------------------------------------------------------------------------------------------
-- Tempplates for WSS data
------------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "wss_aggTrade{S}" (
    "_EventTime" BIGINT,
    "_AggregateTradeID" BIGINT,
    "_Price" NUMERIC,
    "_Quantity" NUMERIC,
    "_FirstTradeID" BIGINT,
    "_LastTradeID" BIGINT,
    "_TradeTime" BIGINT,
    "_IsTheBuyerTheMarketMaker" BOOLEAN,
    "_Ignore" BOOLEAN
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_trade{S}" (
    "_EventTime" BIGINT,
    "_TradeID" BIGINT,
    "_Price" NUMERIC,
    "_Quantity" NUMERIC,
    "_BuyerOrderID" BIGINT,
    "_SellerOrderID" BIGINT,
    "_TradeTime" BIGINT,
    "_IsTheBuyerTheMarketMaker" BOOLEAN,
    "_Ignore" BOOLEAN
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_kline{S}_{I}" (
    "_eventTime" BIGINT,
    "_startTime" BIGINT,
    "_closeTime" BIGINT,
    "_firstTradeId" BIGINT,
    "_lastTradeId" BIGINT,
    "_openPrice" NUMERIC,
    "_closePrice" NUMERIC,
    "_highPrice" NUMERIC,
    "_lowPrice" NUMERIC,
    "_baseAssetVolume" NUMERIC,
    "_numberOfTrades" BIGINT,
    "_klineClosed" BOOLEAN,
    "_quoteAssetVolume" NUMERIC,
    "_takerBuyBaseAssetVolume" NUMERIC,
    "_taherBuyQuoteAssetVolume" NUMERIC,
    "_ignoreField" BIGINT
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_24hrMiniTicker{S}" (
    "_eventTime" BIGINT,
    "_currentDayClosePrice" NUMERIC,
    "_openPrice" NUMERIC,
    "_highPrice" NUMERIC,
    "_lowPrice" NUMERIC,
    "_totalTradedBaseAssetVolume" NUMERIC,
    "_totalTradedQuoteAssetVolume" NUMERIC
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_24hrTicker{S}" (
    "_eventTime" BIGINT,
    "_priceChange" NUMERIC,
    "_priceChangePercent" NUMERIC,
    "_weightedAveragePrice" NUMERIC,
    "_previousDaysClosePrice" NUMERIC,
    "_currentDaysClosePrice" NUMERIC,
    "_closeTradesQuantity" NUMERIC,
    "_bestBidPrice" NUMERIC,
    "_bestBidQuantity" NUMERIC,
    "_bestAskPrice" NUMERIC,
    "_bestAskQuantity" NUMERIC,
    "_openPrice" NUMERIC,
    "_highPrice" NUMERIC,
    "_lowPrice" NUMERIC,
    "_totalTradedBaseAssetVolume" NUMERIC,
    "_totalTradedQuoteAssetVolume" NUMERIC,
    "_statisticsOpenTime" BIGINT,
    "_statisticsCloseTime" BIGINT,
    "_firstTradeID" BIGINT,
    "_lastTradeId" BIGINT,
    "_totalNumberOfTrades" BIGINT
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_depth{S}5" (
    "_lastUpdateId" BIGINT,
    "_bids" JSONB,
    "_asks" JSONB
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_depth{S}10" (
    "_lastUpdateId" BIGINT,
    "_bids" JSONB,
    "_asks" JSONB
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_depth{S}20" (
    "_lastUpdateId" BIGINT,
    "_bids" JSONB,
    "_asks" JSONB
); COMMIT;

CREATE TABLE IF NOT EXISTS "wss_depth{S}" (
    "_eventTime" BIGINT,
    "_firstUpdateID" BIGINT,
    "_finalUpdateID" BIGINT,
    "_bids" JSONB,
    "_asks" JSONB
); COMMIT;
*/
