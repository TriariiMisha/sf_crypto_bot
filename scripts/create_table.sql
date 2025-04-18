CREATE TABLE public.bybit_records (
    sync_ts BIGINT NOT NULL,      -- системный timestamp, один на итерацию цикла
    symbol VARCHAR(20) NOT NULL,
    timestamp BIGINT,
    best_bid_price FLOAT,
    best_bid_volume FLOAT,
    best_ask_price FLOAT,
    best_ask_volume FLOAT,
    PRIMARY KEY (sync_ts, symbol)
);