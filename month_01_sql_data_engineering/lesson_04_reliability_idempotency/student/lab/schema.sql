DROP VIEW IF EXISTS gold_daily_sales;
DROP VIEW IF EXISTS silver_orders;
DROP VIEW IF EXISTS current_order_state;
DROP VIEW IF EXISTS deduped_order_changes;

DROP TABLE IF EXISTS bronze_order_changes;

CREATE TABLE bronze_order_changes (
    change_id TEXT NOT NULL,
    operation TEXT NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    amount REAL,
    change_timestamp TEXT NOT NULL
);