INSERT INTO customers (customer_id, customer_name, email, created_at) VALUES
    (1, 'Anna Kowalska', 'anna@team.com', '2024-01-10'),
    (2, 'Jan Nowak', 'jan@team.com', '2024-01-12'),
    (3, 'Maria Zielinska', 'maria@team.com', '2024-02-03'),
    (4, 'Piotr Wisniewski', 'piotr@team.com', '2024-02-20'),
    (5, 'Ewa Lewandowska', 'ewa@team.com', '2024-03-01');

INSERT INTO products (product_id, product_name, category, unit_price) VALUES
    (1, 'Laptop Pro 14', 'electronics', 6200.00),
    (2, 'Monitor 27', 'electronics', 1200.00),
    (3, 'Office Chair', 'furniture', 850.00),
    (4, 'Desk Lamp', 'furniture', 140.00),
    (5, 'Noise Cancelling Headphones', 'electronics', 900.00),
    (6, 'Standing Desk', 'furniture', 1800.00),
    (7, 'USB-C Hub', 'electronics', 220.00);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
    (101, 1, '2024-03-05', 'paid'),
    (102, 1, '2024-03-12', 'paid'),
    (103, 2, '2024-03-12', 'cancelled'),
    (104, 2, '2024-03-14', 'paid'),
    (105, 3, '2024-03-15', 'paid'),
    (106, 3, '2024-03-15', 'paid'),
    (107, 4, '2024-03-20', 'paid');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (1001, 101, 1, 1, 6200.00),
    (1002, 101, 2, 2, 1200.00),
    (1003, 102, 5, 1, 900.00),
    (1004, 103, 3, 1, 850.00),
    (1005, 104, 4, 2, 140.00),
    (1006, 104, 5, 1, 900.00),
    (1007, 105, 2, 1, 1200.00),
    (1008, 106, 6, 1, 1800.00),
    (1009, 107, 3, 2, 850.00);
