-- Lekcja 04: niezawodnosc, idempotencja i zaufanie do danych
-- Najpierw uruchom schema.sql i seed_data.sql.
-- Tryb pracy: przy kazdym kroku zapisz klucz, grain, zachowanie przy retry i check, ktory wykrywa blad.
-- Pipeline jest poprawny dopiero wtedy, gdy drugi run na tym samym input nie podwaja Gold.

-- Zadanie 1: duplicate event check
-- Cel: sprawdz, czy source wyslal ten sam event wiecej niz raz.
-- Expected: change_id = chg_002 ma records_count = 2.
-- TODO: napisz SELECT grupujacy po change_id i filtrujacy COUNT(*) > 1.


-- Zadanie 2: deduped_order_changes
-- Grain: jeden rekord = jeden unikalny change_id.
-- Key: change_id deduplikuje event CDC.
-- Retry guarantee: duplicate event nie przejdzie dalej dwa razy.
-- Hint: uzyj ROW_NUMBER() OVER (PARTITION BY change_id ORDER BY change_timestamp DESC, order_id DESC).
-- TODO: CREATE VIEW deduped_order_changes AS ...


-- Zadanie 3: current_order_state
-- Grain: jeden rekord = jeden najnowszy stan per order_id.
-- Key: order_id jest business key zamowienia.
-- Retry guarantee: wiele zmian jednego order_id daje jeden aktualny stan.
-- Hint: uzyj ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY change_timestamp DESC, change_id DESC).
-- TODO: CREATE VIEW current_order_state AS ...


-- Zadanie 4: silver_orders
-- Grain: jeden rekord = jeden aktywny order_id.
-- Key: order_id.
-- Retry guarantee: DELETE nie zostaje aktywnym zamowieniem po ponownym przeliczeniu.
-- TODO: CREATE VIEW silver_orders AS SELECT ... FROM current_order_state WHERE operation <> 'DELETE'.


-- Zadanie 5: gold_daily_sales
-- Grain: jeden rekord = jeden order_date.
-- Key: order_date jako dzien biznesowy raportu.
-- Retry guarantee: Gold jest liczony z current state, wiec duplicate event nie podwaja revenue.
-- TODO: CREATE VIEW gold_daily_sales AS SELECT order_date, COUNT(*), SUM(amount) ... WHERE status = 'paid'.


-- Zadanie 6: validation checks
-- Dodaj zapytania, ktore powinny zwracac 0 wierszy:
-- 1. duplicate order_id w silver_orders,
-- 2. null order_id/customer_id/order_date,
-- 3. negative amount,
-- 4. unexpected status,
-- 5. revenue sanity: suma Silver paid = suma Gold.


-- Zadanie 7: retry explanation
-- W komentarzu odpowiedz:
-- Co podwoiloby revenue w naiwnym pipeline?
-- Ktory krok w twoim projekcie temu zapobiega?
-- Jaki check wykryje podwojenie?