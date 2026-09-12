-- SQL basics extra tasks
-- Opcjonalna powtorka podstaw SQL przed homeworkiem.
-- To jest cwiczenie pomocnicze. Wpisz odpowiedzi w tym pliku i dodaj go do PR.
-- Uzyj go, jesli chcesz spokojnie przejsc przez podstawowa skladnie przed lab/02.
-- Uzyj tabel z schema.sql i danych z seed_data.sql.
-- Jesli cwiczysz DDL, uzywaj tylko tabeli testowej tmp_sql_refresh.
-- Minimum: zadania 1-10, czyli SELECT, WHERE, ORDER BY, GROUP BY i JOIN.
-- Bonus po minimum: zadania 11-18.

-- Zadanie 1
-- Wyswietl wszystkie kolumny z tabeli customers.


-- Zadanie 2
-- Wyswietl tylko customer_id, customer_name i email z tabeli customers.


-- Zadanie 3
-- Uzyj aliasu dla kolumny email jako customer_email.


-- Zadanie 4
-- Wyswietl zamowienia ze statusem 'paid'.


-- Zadanie 5
-- Wyswietl 3 najnowsze zamowienia.


-- Zadanie 6
-- Posortuj produkty od najdrozszego do najtanszego.


-- Zadanie 7
-- Policz liczbe zamowien per status.


-- Zadanie 8
-- Pokaz tylko te statusy, ktore maja wiecej niz jedno zamowienie.


-- Zadanie 9
-- Polacz customers z orders i pokaz customer_name, order_id, order_date, status.


-- Zadanie 10
-- Uzyj LEFT JOIN, aby pokazac wszystkich klientow i ich zamowienia, jesli istnieja.


-- BONUS: zadania 11-18 sa dodatkowe.

-- Zadanie 11
-- Polacz nazwy klientow i nazwy produktow w jedna kolumne name przy pomocy UNION.


-- Zadanie 12
-- Stworz tabele tmp_sql_refresh z kolumnami: id, label, created_at.


-- Zadanie 13
-- Dodaj jeden rekord do tmp_sql_refresh.


-- Zadanie 14
-- Zmien label w tmp_sql_refresh.


-- Zadanie 15
-- Usun tmp_sql_refresh przez DROP TABLE IF EXISTS.


-- Zadanie 16
-- Policz revenue/przychod dla kazdego produktu.


-- Zadanie 17
-- Policz liczbe unikalnych klientow, ktorzy kupili produkt z kategorii electronics.


-- Zadanie 18
-- Znajdz klientow bez zadnego zamowienia paid.
