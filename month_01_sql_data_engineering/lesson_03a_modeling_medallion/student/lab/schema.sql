DROP VIEW IF EXISTS gold_sales_by_region_category;
DROP VIEW IF EXISTS gold_daily_sales;
DROP VIEW IF EXISTS fact_sales;
DROP VIEW IF EXISTS dim_product;
DROP VIEW IF EXISTS dim_customer;

DROP TABLE IF EXISTS raw_order_items;
DROP TABLE IF EXISTS raw_orders;
DROP TABLE IF EXISTS raw_products;
DROP TABLE IF EXISTS raw_customers;

CREATE TABLE raw_customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE raw_products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    active_flag INTEGER NOT NULL
);

CREATE TABLE raw_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    channel TEXT NOT NULL
);

CREATE TABLE raw_order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);