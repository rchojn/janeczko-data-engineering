INSERT INTO raw_customers (customer_id, customer_name, region, created_at) VALUES
(1, 'Anna Kowalska', 'north', '2025-12-01'),
(2, 'Bartek Nowak', 'south', '2025-12-05'),
(3, 'Celina Zielinska', 'west', '2025-12-10'),
(4, 'Daniel Wisniewski', 'east', '2025-12-12');

INSERT INTO raw_products (product_id, product_name, category, active_flag) VALUES
(10, 'Keyboard', 'accessories', 1),
(11, 'Mouse', 'accessories', 1),
(12, 'Monitor', 'hardware', 1),
(13, 'USB-C Cable', 'accessories', 1),
(14, 'Laptop Stand', 'office', 1);

INSERT INTO raw_orders (order_id, customer_id, order_date, status, channel) VALUES
(100, 1, '2026-01-01', 'paid', 'web'),
(101, 1, '2026-01-02', 'paid', 'mobile'),
(102, 2, '2026-01-02', 'cancelled', 'web'),
(103, 3, '2026-01-03', 'paid', 'partner'),
(104, 4, '2026-01-04', 'refunded', 'web'),
(105, 2, '2026-01-05', 'paid', 'mobile'),
(106, 3, '2026-01-06', 'paid', 'web');

INSERT INTO raw_order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 100, 10, 1, 120.0),
(2, 100, 11, 2, 80.0),
(3, 101, 12, 1, 900.0),
(4, 102, 13, 3, 30.0),
(5, 103, 14, 2, 150.0),
(6, 104, 11, 1, 80.0),
(7, 105, 10, 1, 120.0),
(8, 105, 13, 4, 30.0),
(9, 106, 12, 2, 900.0);