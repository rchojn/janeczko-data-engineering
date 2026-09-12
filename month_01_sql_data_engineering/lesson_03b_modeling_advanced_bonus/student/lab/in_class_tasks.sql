-- Bonus 03b: zaawansowane pojęcia modelowania
-- Ten lab używa małych CTE. Nie wymaga osobnej bazy.

-- =====================================================================
-- ZADANIE 1: surrogate key vs business key
-- =====================================================================
-- Zbuduj CTE dim_customer_scd2 z kolumnami:
-- customer_sk, customer_id, region, valid_from, valid_to, is_current.
--
-- Pytanie:
-- Dlaczego customer_id nie wystarcza jako jedyny klucz, gdy mamy historię?


-- =====================================================================
-- ZADANIE 2: conformed dimension
-- =====================================================================
-- Zbuduj CTE dim_date oraz dwa małe facty:
-- fact_sales_daily i fact_returns_daily.
--
-- Pytanie:
-- Dlaczego oba facty powinny używać tej samej dim_date?


-- =====================================================================
-- ZADANIE 3: typy fact tables
-- =====================================================================
-- Opisz w komentarzu grain:
-- fact_sales: transaction fact = ...
-- fact_inventory_daily: periodic snapshot fact = ...
-- fact_order_lifecycle: accumulating snapshot fact = ...


-- =====================================================================
-- ZADANIE 4: additive vs non-additive
-- =====================================================================
-- Pokaż przykład, gdzie AVG(conversion_rate) jest błędne.
-- Policz poprawną metrykę jako SUM(conversions) / SUM(visits).


-- =====================================================================
-- ZADANIE 5: bridge table
-- =====================================================================
-- Zbuduj CTE:
-- dim_product(product_id, product_name)
-- dim_tag(tag_id, tag_name)
-- bridge_product_tag(product_id, tag_id)
-- fact_sales(product_id, line_revenue)
--
-- Pytanie:
-- Jak wygląda ścieżka joinu od fact_sales do dim_tag?
-- Dlaczego revenue może się podwoić, jeśli produkt ma kilka tagów?


-- =====================================================================
-- ZADANIE 6: semantic layer
-- =====================================================================
-- Napisz w komentarzu definicję metryki paid_revenue.
--
-- paid_revenue = ...
--
-- Pytanie:
-- Dlaczego ta definicja powinna być centralna, a nie kopiowana w 10 dashboardach?
