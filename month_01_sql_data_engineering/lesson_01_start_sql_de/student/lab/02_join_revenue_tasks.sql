-- Lekcja 01: JOIN, revenue/przychod i customer_order_summary
-- Cwiczenie pomocnicze do homework/lesson_01/01_solution.sql.
-- Wpisz odpowiedzi w tym pliku i dodaj go do PR.
-- Uzyj go, jesli finalne query w homeworku jest jeszcze za duzym skokiem.
-- Zadania 0-8 ida od malych SELECT-ow do finalnego customer_order_summary.
-- Po kazdym zadaniu uruchom query i zobacz wynik, zanim przejdziesz dalej.
-- Uzywasz danych z schema.sql i seed_data.sql.
-- Tabele:
-- customers, orders, order_items, products.
-- W tym pliku piszesz tylko SELECT-y.

-- Zadanie 0
-- Sprawdz liczbe rekordow w kazdej tabeli.


-- Zadanie 1
-- Pokaz kilka rekordow z kazdej tabeli przez SELECT *.


-- Zadanie 2
-- Pokaz tylko zamowienia ze statusem 'paid'.
-- Tabela: orders.


-- Zadanie 3
-- Policz liczbe zamowien per status.
-- Tabela: orders.
-- Podpowiedz: GROUP BY status.


-- Zadanie 4
-- Polacz customers z orders.
-- Wynik: customer_id, customer_name, order_id, order_date, status.


-- Zadanie 5
-- Policz revenue/przychod dla kazdego zamowienia.
-- Tabele: orders + order_items.
-- Revenue liczymy tak:
-- quantity * unit_price
--
-- Wynik: order_id, customer_id, status, order_revenue.


-- Zadanie 6
-- Policz revenue/przychod dla kazdego klienta tylko dla zamowien paid.
-- Tabele: customers + orders + order_items.
-- Pamietaj: zamowienie cancelled nie wchodzi do revenue/przychodu.
--
-- Wynik: customer_id, customer_name, total_revenue.


-- Zadanie 7
-- Sprawdz, ile rekordow jest w orders przed joinem z order_items.
-- Potem sprawdz, ile rekordow jest po joinie.


-- Zadanie 8
-- Napisz finalne query customer_order_summary.
-- Grain wyniku: jeden rekord = jeden klient.
--
-- Wynik ma miec kolumny:
-- customer_id
-- customer_name
-- orders_count
-- total_revenue
-- last_order_date
--
-- Zasady:
-- - licz tylko zamowienia paid,
-- - revenue = quantity * unit_price,
-- - klient bez zamowien paid powinien zostac w wyniku z total_revenue = 0.


-- Bonus, tylko jesli zadania 0-8 sa jasne.
-- CTE jest pokazane w slides.presenterm.md i teoria.md jako dodatek, nie minimum.
-- 1. Znajdz produkty, ktore nigdy nie zostaly kupione w zamowieniu paid.
-- 2. Przepisz finalne query na CTE.
