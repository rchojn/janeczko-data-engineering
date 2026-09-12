-- Lekcja 02 używa podobnego modelu jak lekcja 01: customers -> orders -> order_items -> products.
-- To nie jest jednak dokładnie ta sama schema.
-- Różnice pod ćwiczenia performance/advanced SQL:
--   1. orders ma kolumnę channel, żeby liczyć revenue per channel.
--   2. orders ma order_date jako TEXT, żeby filtrować zakres dat w SQLite.
--   3. order_items trzyma unit_price, żeby revenue liczyć jako quantity * unit_price.
--   4. Dodajemy indeksy, żeby EXPLAIN QUERY PLAN mógł pokazać różnicę między SCAN i SEARCH.
--
-- Najważniejsze: indeksy nie są pierwszą odpowiedzią na każde wolne query.
-- Tu są dodane celowo jako materiał do obserwacji planu wykonania.

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    channel TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indeks po dacie pomaga przy filtrach typu:
-- WHERE order_date >= '2026-01-01' AND order_date < '2026-01-06'
CREATE INDEX idx_orders_date ON orders(order_date);

-- Indeks po statusie pomaga przy filtrze:
-- WHERE status = 'paid'
CREATE INDEX idx_orders_status ON orders(status);

-- Indeks po order_id w order_items pomaga przy joinie:
-- orders.order_id = order_items.order_id
CREATE INDEX idx_order_items_order_id ON order_items(order_id);