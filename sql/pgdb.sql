----------------------------------------------------------------------------------------------------------------------------------
-- Create data types
----------------------------------------------------------------------------------------------------------------------------------
DROP TYPE IF EXISTS security_type; COMMIT;
CREATE TYPE security_type AS ENUM ('NONE','TRADE','USER_DATA','USER_STREAM','MARKET_DATA');

DROP TYPE IF EXISTS symbol_status; COMMIT;
CREATE TYPE symbol_status AS ENUM ('PRE_TRADING','TRADING','POST_TRADING','END_OF_DAY','HALT','AUCTION_MATCH','BREAK');

DROP TYPE IF EXISTS symbol_type; COMMIT;
CREATE TYPE symbol_type AS ENUM ('SPOT');

DROP TYPE IF EXISTS order_status; COMMIT;
CREATE TYPE order_status AS ENUM ('NEW','PARTIALLY_FILLED','FILLED','CANCELED','PENDING_CANCEL','REJECTED','EXPIRED');

DROP TYPE IF EXISTS order_type; COMMIT;
CREATE TYPE order_type AS ENUM ('LIMIT','MARKET','STOP_LOSS','STOP_LOSS_LIMIT','TAKE_PROFIT','TAKE_PROFIT_LIMIT','LIMIT_MAKER');

DROP TYPE IF EXISTS order_side; COMMIT;
CREATE TYPE order_side AS ENUM ('BUY','SELL');

DROP TYPE IF EXISTS time_in_force; COMMIT;
CREATE TYPE time_in_force AS ENUM ('GTC','IOC','FOK');

DROP TYPE IF EXISTS kline_intervals; COMMIT;
CREATE TYPE kline_intervals AS ENUM ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w','1M');

DROP TYPE IF EXISTS rate_limiter; COMMIT;
CREATE TYPE rate_limiter AS ENUM ('REQUESTS', 'ORDERS');

DROP TYPE IF EXISTS rate_limit_intervals; COMMIT;
CREATE TYPE rate_limit_intervals AS ENUM ('SECOND', 'MINUTE', 'DAY');
