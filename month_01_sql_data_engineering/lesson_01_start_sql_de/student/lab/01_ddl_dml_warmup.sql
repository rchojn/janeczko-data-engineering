-- DDL/DML warm-up
-- Cel: pocwiczyc CREATE, INSERT, UPDATE, ALTER, SELECT i DROP.
-- To jest opcjonalne cwiczenie pomocnicze do homeworku.
-- Jesli je robisz, wpisz odpowiedzi w tym pliku i dodaj go do PR.
-- Uzyj go wtedy, gdy chcesz osobno pocwiczyc DDL/DML przed homeworkiem.
-- Po tym pliku masz umiec powiedziec: ktore komendy zmienily strukture, a ktore dane.
-- Pracujesz na osobnej tabeli testowej test_orders.
-- Nie zmieniasz tabel customers/orders/order_items/products.

-- Zadanie 1
-- Utworz tabele test_orders.
-- Kolumny:
-- raw_order_id, customer_email, order_date, amount, load_status


-- Zadanie 2
-- Dodaj 3 przykladowe rekordy.
-- Uzyj statusow: 'new', 'invalid', 'new'.


-- Zadanie 3
-- Zmien status rekordow 'new' na 'processed'.


-- Zadanie 4
-- Sprawdz ile rekordow jest w kazdym statusie.


-- Zadanie 5
-- Dodaj kolumne source_file typu TEXT.


-- Zadanie 6
-- Uzupelnij source_file dla wszystkich rekordow wartoscia 'manual_seed.csv'.


-- Zadanie 7
-- Usun tabele test_orders przez DROP TABLE IF EXISTS.


-- Pytania
-- 1. Ktore komendy byly DDL?
-- 2. Ktore komendy byly DML?
-- 3. Jak sprawdzisz, czy UPDATE albo INSERT zadzialal?
