-- Lekcja 03: model analityczny e-commerce
-- Najpierw uruchom schema.sql i seed_data.sql.
-- Tryb pracy: przed każdym CREATE VIEW zapisz grain i purpose.

-- =====================================================================
-- ZADANIE 1: raw/Bronze grain
-- =====================================================================
-- Opisz w komentarzu grain:
-- raw_customers: jeden rekord = ...
-- raw_products: jeden rekord = ...
-- raw_orders: jeden rekord = ...
-- raw_order_items: jeden rekord = ...


-- =====================================================================
-- ZADANIE 2: Silver views
-- =====================================================================
-- Stwórz:
-- 1. silver_customers,
-- 2. silver_products,
-- 3. silver_orders.
--
-- Silver ma być prosty: jawne kolumny, TRIM/LOWER dla tekstu,
-- bez SELECT * jako głównego wzorca modelu.
--
-- Przykład decyzji:
-- raw_orders.status -> LOWER(TRIM(status)) AS status


-- =====================================================================
-- ZADANIE 3: dimensions
-- =====================================================================
-- Stwórz dim_customer i dim_product na podstawie Silver.
-- Dimensions trzymają kontekst, nie metryki typu revenue.
--
-- dim_customer: jeden rekord = ...
-- dim_product: jeden rekord = ...


-- =====================================================================
-- ZADANIE 4: fact_sales
-- =====================================================================
-- Stwórz fact_sales tylko dla paid orders.
-- Grain: jeden rekord = jedna pozycja opłaconego zamówienia.
-- Revenue: quantity * unit_price.
--
-- Pytanie kontrolne:
-- Dlaczego fact_sales ma być na poziomie order_item, a nie order_id?


-- =====================================================================
-- ZADANIE 5: gold_daily_sales
-- =====================================================================
-- Stwórz gold_daily_sales.
-- Grain: jeden rekord = jeden order_date.
-- To jest gotowa tabela pod prosty dashboard dziennej sprzedaży.


-- =====================================================================
-- ZADANIE 6: gold_sales_by_region_category
-- =====================================================================
-- Stwórz bardziej analityczny Gold.
-- Grain: jeden rekord = jeden dzień + region klienta + kategoria produktu.
--
-- Kolumny:
-- order_date, region, category, total_revenue, order_count, line_count
--
-- Pytanie kontrolne:
-- Które kolumny muszą być w GROUP BY, żeby grain był poprawny?


-- =====================================================================
-- ZADANIE 7: star schema query vs Gold query
-- =====================================================================
-- Napisz dwa SELECT-y:
-- 1. revenue per region i category z fact_sales + dim_customer + dim_product,
-- 2. revenue per region i category z gold_sales_by_region_category.
--
-- Dopisz komentarz:
-- Kiedy star schema jest lepszy?
-- Kiedy gotowy Gold jest lepszy?


-- =====================================================================
-- ZADANIE 8: quality checks
-- =====================================================================
-- Dodaj SELECT-y kontrolne:
-- 1. duplicate customer_id w dim_customer,
-- 2. duplicate product_id w dim_product,
-- 3. null keys w fact_sales,
-- 4. suma revenue w fact_sales vs suma revenue w gold_daily_sales,
-- 5. brak statusów innych niż paid w fact_sales,
-- 6. brak ujemnego line_revenue,
-- 7. suma revenue w fact_sales vs suma revenue w gold_sales_by_region_category.


-- =====================================================================
-- ZADANIE 9: mini-decyzja o historii wymiaru
-- =====================================================================
-- Nie implementuj historii wymiaru w SQL.
-- Odpowiedz w komentarzu albo w model_design.md:
-- 1. Co robimy, jeśli customer zmienia region?
-- 2. Kiedy wystarczy aktualny opis klienta?
-- 3. Kiedy raport potrzebuje historycznego opisu z dnia sprzedaży?


-- Jeśli chcesz przećwiczyć SCD Type 2, przejdź do bonusu 03b.
-- Tam są business key, surrogate key, valid_from/valid_to i join po dacie.
