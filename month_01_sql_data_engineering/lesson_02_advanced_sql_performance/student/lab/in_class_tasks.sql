-- Lekcja 02: advanced SQL + performance mindset
-- Uruchom najpierw: schema.sql, potem seed_data.sql.
-- Pracuj krótko: napisz query -> uruchom -> dopisz 1-2 zdania obserwacji.

-- =====================================================================
-- ZADANIE 1: EXPLAIN orders per status
-- =====================================================================
-- Napisz EXPLAIN QUERY PLAN dla liczby zamówień per status.
-- Grain wyniku: jeden status.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 2: SELECT * vs jawne kolumny
-- =====================================================================
-- Porównaj EXPLAIN dla SELECT * i SELECT jawnych kolumn z orders.
-- Filtr dat: 2026-01-01 <= order_date < 2026-01-06.
-- Jawne kolumny: order_id, customer_id, order_date, status, channel.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 3: paid revenue per channel
-- =====================================================================
-- Policz revenue per channel tylko dla status = 'paid'.
-- Grain wyniku: jeden channel.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 4: paid revenue per channel przez CTE
-- =====================================================================
-- Przepisz zadanie 3 przez CTE: paid_orders -> order_revenue -> finalny SELECT.
-- Przy CTE dopisz krótko grain.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 5: daily paid revenue
-- =====================================================================
-- Policz daily revenue dla status = 'paid'.
-- Grain wyniku: jeden order_date.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 6: running total
-- =====================================================================
-- Do daily revenue dodaj running total przez window function.
-- Użyj: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.


-- Obserwacja:

-- =====================================================================
-- ZADANIE 7: jedna zmiana naraz
-- =====================================================================
-- Porównaj EXPLAIN dla revenue per channel bez filtra statusu i z filtrem status = 'paid'.


-- Obserwacja:
