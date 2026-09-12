---
title: SQL, data flow i rola Data Engineera
author: Lesson 01
date: 2026-07-12

---

# SQL, data flow i rola Data Engineera

## Pierwsza lekcja merytoryczna

Cel: nie tylko napisac query, ale wiedziec co ono znaczy.

<!-- end_slide -->
# Zanim zaczniemy SQL

W tej lekcji pilnujemy jednego pytania:

```text
Co oznacza wynik query?
```

```text
tabela  = dane w wierszach i kolumnach
JOIN    = polaczenie tabel
grain   = co oznacza jeden rekord
```

Warstwy platformy danych wroca pozniej.
Teraz skupiamy sie na malym modelu danych.

<!-- end_slide -->

# Problem biznesowy

Sklep pyta:

```text
Ile zarobilismy?
Ktore produkty sprzedaja sie najlepiej?
Ktorzy klienci wracaja?
Czy metryka jest policzona tak samo jak tydzien temu?
```

SQL odpowiada na pytanie.

Data Engineering sprawia, ze odpowiedz jest powtarzalna i zaufana.

<!-- end_slide -->

# Od aplikacji do metryki

```text
Application
  -> writes orders
  -> writes order_items
  -> zapisuje dane transakcyjne

Production DB
  -> stores current transactional state

Data platform
  -> snapshots / CDC
  -> cleans data
  -> models metrics
```

<!-- end_slide -->

# Gdzie w tym SQL?

SQL pojawia sie w wielu miejscach:

- sprawdzenie danych zrodlowych,
- laczenie tabel,
- liczenie metryk,
- testy jakosci,
- odpowiedz interview.

SQL to nie tylko raport. To jezyk kontroli danych.

<!-- end_slide -->

# E-commerce dataset

Bedziemy uzywac jednego case'u:

```text
customers
orders
order_items
products
```

Jeden dataset pozwala widziec progres: tabele -> joiny -> metryki -> walidacja.

<!-- end_slide -->

# Najpierw relacje

Zanim zrobisz JOIN — musisz wiedziec PO CZYM laczyc tabele.

```text
PK = Primary Key: unikalny identyfikator wiersza w tej tabeli
FK = Foreign Key: odwolanie do PK w innej tabeli
```

JOIN laczy tabele po PK ↔ FK.

<!-- end_slide -->

# Relacje w datasetcie

```text
customers  customer_id (PK)
               └─► orders  customer_id (FK)  order_id (PK)
                                   └─► order_items  order_id (FK)

products   product_id (PK)
               └─► order_items  product_id (FK)
```

Jesli polaczysz po zlej kolumnie:

```text
query odpali sie poprawnie,
ale wynik bedzie biznesowo bezsensowny.
```

<!-- end_slide -->

# DDL vs DML

SQL robi dwie rozne rzeczy:

```sql
-- DDL: zmienia STRUKTURE tabeli
CREATE TABLE test_orders (...);
ALTER TABLE test_orders ADD COLUMN source_file TEXT;
DROP TABLE IF EXISTS test_orders;

-- DML: zmienia DANE w tabeli
SELECT * FROM orders;
INSERT INTO test_orders VALUES (...);
UPDATE test_orders SET status = 'paid';
DELETE FROM test_orders WHERE id = 1;
```

<!-- end_slide -->

# DDL vs DML: zapamietaj

W tej lekcji:

```text
DDL = zmieniasz strukture tabeli testowej
DML = czytasz albo zmieniasz dane
```

Uwaga: ten sam INSERT dwa razy = duplikaty.
Na razie tylko zapamietaj: po INSERT/UPDATE zawsze sprawdz wynik SELECT-em.

<!-- end_slide -->

# Grain: najwazniejsze slowo

```text
Grain = co oznacza jeden rekord?
```

Przyklad:

```text
Tabela        Grain = jeden rekord oznacza...
------------  --------------------------------
customers     jednego klienta
orders        jedno zamowienie
order_items   jedna pozycje zamowienia
products      jeden produkt
```

<!-- end_slide -->

# Dlaczego grain ratuje wynik?

Rozny grain = rozna liczba wierszy:

```text
orders                 order_items
────────────────       ──────────────────────────────────
order_id  status       order_item_id  order_id  qty  price
   1      paid   ────►      1            1       2    500
                  └───►      2            1       1     50
   2      paid   ────►      3            2       3     20

COUNT(orders)      = 2
COUNT(order_items) = 3   ← zawsze sprawdz przed i po joinie!
```

Join `orders → order_items` zwieksza liczbe wierszy.

<!-- end_slide -->

# Grain: dobra praktyka

**Dobra praktyka:**
- przed joiniem: `SELECT COUNT(*) FROM orders`
- po joinie: `SELECT COUNT(*) FROM orders JOIN order_items USING (order_id)`
- napisz grain wyniku jednym zdaniem ZANIM zaczniesz pisac query

**Nie rob:**
- nie zakladaj, ze join nie zmienil grain
- nie licz `SUM(unit_price)` bez sprawdzenia czy rekord sie nie podwoil

<!-- end_slide -->

# Grain i JOIN wizualnie

```text
orders                      order_items
--------------------        ---------------------------------
order_id | status           item_id | order_id | qty | price
---------+--------          --------+----------+-----+------
101      | paid      -----> 1001    | 101      | 1   | 6200
101      | paid      -----> 1002    | 101      | 2   | 1200
102      | paid      -----> 1003    | 102      | 1   | 900

Po JOIN orders -> order_items:
  wynik       = 3 wiersze   (grain: 1 pozycja zamowienia)
```

TAK — JOIN zmienil grain wyniku:

```text
przed JOIN:  grain = 1 zamowienie   (orders: 2 wiersze)
po JOIN:     grain = 1 pozycja      (order_items: 3 wiersze)
```

Order 101 pojawia sie dwa razy, bo ma 2 pozycje.
Jesli teraz policzysz `COUNT(*)` — liczysz pozycje, nie zamowienia.

<!-- end_slide -->

# Query moze byc poprawne skladniowo i zle biznesowo

SQL moze sie odpalic i dalej dac zla liczbe.

```text
Blad techniczny?     Query sie nie odpala.
Blad biznesowy?      Query sie odpala, ale liczba znaczy cos innego.
```

Prosty test:

```text
Czy umiesz powiedziec jednym zdaniem,
co oznacza 1 wiersz wyniku?
```

<!-- end_slide -->

# Przyklady bledow biznesowych

```text
Problem                    Dlaczego wynik jest zly?
------------------------   -----------------------------------------------
orders JOIN order_items    1 order ma wiele pozycji, wiec order sie powtarza
canceled w sales           cancelled oznacza: klient nie kupil
SUM(unit_price)            cena jednej sztuki != wartosc calej pozycji
COUNT(*) po JOIN           po JOIN liczysz pozycje, nie zamowienia
brak grain wyniku          nie wiesz czy 1 wiersz = customer/order/item
```

<!-- end_slide -->

# SQL mindset

Przed query zapytaj:

```text
1. Jakie pytanie biznesowe odpowiadam?
2. Co oznacza jeden rekord wejscia?
3. Co oznacza jeden rekord wyniku?
4. Jak definiuje metryke?
5. Jak sprawdze, ze wynik ma sens?
```

<!-- end_slide -->

# SQL ma dwa porzadki

Piszesz zwykle tak:

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...
```

Ale logicznie baza mysli inaczej.

<!-- end_slide -->

# Logiczny przeplyw SQL

Silnik bazodanowy przetwarza query w tej kolejnosci:

```text
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT

FROM      skad bierzesz dane
WHERE     ktore rekordy wyrzucasz
GROUP BY  po czym grupujesz
HAVING    filtr gotowych grup
SELECT    co pokazujesz
ORDER BY  kolejnosc wyniku
LIMIT     ile wierszy
```

Alias z `SELECT` nie dziala w `WHERE`.
`SELECT` jest przetwarzany dopiero po `WHERE`.

<!-- end_slide -->

# Logiczny przeplyw: mnemonik

Zdanie do zapamiętania:

```text
FROM WHERE GROUPS HAVE SELECTED ORDERS LIMITS

Po polsku:
"Skad grupy maja wybrane zamowienia z limitami."
```

<!-- end_slide -->

# Build 1: skad dane i ktore rekordy

```text
FROM / JOIN   ← skad bierzesz dane
  -> WHERE    ← ktore rekordy wyrzucasz
```

Najpierw wybierasz z jakich tabel i ktore rekordy chcesz.
Dopiero potem grupujesz i liczysz metryki.

```text
FROM      WHERE     GROUP BY   HAVING    SELECT    ORDER BY   LIMIT
skad      ktore     po czym    majac     co        posortuj   ile

FROM WHERE GROUPS HAVE SELECTED ORDERS LIMITS
Po polsku: "Skad grupy maja wybrane zamowienia z limitami."
```

<!-- end_slide -->

# Build 2: grupy i filtr na grupach

```text
FROM / JOIN
  -> WHERE    ← filtr surowych rekordow
  -> GROUP BY
  -> HAVING   ← filtr gotowych grup
```

`WHERE` filtruje pojedyncze rekordy przed grupowaniem.
`HAVING` filtruje gotowe grupy po agregacji.

```text
FROM WHERE GROUPS HAVE SELECTED ORDERS LIMITS
Po polsku: "Skad grupy maja wybrane zamowienia z limitami."
```

<!-- end_slide -->

# Build 3: dopiero teraz SELECT

```text
FROM / JOIN
  -> WHERE
  -> GROUP BY
  -> HAVING
  -> SELECT   ← dopiero tutaj powstaja aliasy i nazwy kolumn
  -> ORDER BY
  -> LIMIT
```

Alias z `SELECT` nie istnieje jeszcze w `WHERE`.
`WHERE` jest przetwarzany wczesniej.

<!-- end_slide -->

# Najczestszy blad: alias w WHERE

```sql
SELECT
    quantity * unit_price AS gross_line_value
FROM order_items
WHERE gross_line_value > 100;
```

Co jest nie tak?

<!-- end_slide -->

# Poprawka: powtorz wyrazenie w WHERE

```sql
SELECT
    quantity * unit_price AS gross_line_value
FROM order_items
WHERE quantity * unit_price > 100;
```

`gross_line_value` nie istnieje jeszcze w momencie WHERE.
Baza przetwarza WHERE zanim dotrze do SELECT.
Dlatego musisz powtorzyc wyrazenie.

```text
WHERE jest przed SELECT.
Alias powstaje dopiero w SELECT.
```

<!-- end_slide -->

# Najczestszy blad: WHERE zamiast HAVING

```sql
SELECT customer_id, COUNT(*) AS orders_count
FROM orders
WHERE COUNT(*) > 1
GROUP BY customer_id;
```

Co jest nie tak?

<!-- end_slide -->

# Poprawka: HAVING filtruje grupy

```sql
SELECT customer_id, COUNT(*) AS orders_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

`COUNT(*)` to wynik agregacji.
Powstaje dopiero po GROUP BY.
WHERE nie moze filtrowac czegos, co jeszcze nie istnieje.

```text
HAVING jest po GROUP BY.
WHERE jest przed GROUP BY.
```

<!-- end_slide -->

# Mini brief przed query

Zanim napiszesz SQL, zapisz 5 rzeczy:

```text
1. Brief:
  Ile revenue ma kazdy customer?
2. Tabele:
  customers, orders, order_items
3. Grain wyniku:
  1 wiersz = 1 klient
4. Metryka:
  revenue = SUM(quantity * unit_price)
5. Check:
  1 customer_id wystepuje max 1 raz w wyniku
```

<!-- end_slide -->

# Mini brief: po co?

To jest prosty kontrakt:
- co liczysz,
- z czego,
- na jakim grain,
- jak sprawdzisz wynik.

<!-- end_slide -->

# Revenue: definicja zanim SQL

Zla definicja:

```text
Revenue = amount
```

Lepsza definicja:

```text
Revenue = sum(order_items.quantity * order_items.unit_price)
Tylko zamowienia ze statusem paid.
Nie licz cancelled, jesli nie ustalono inaczej.
Grain wyniku: jeden wiersz na klienta.
```

<!-- end_slide -->

# Revenue jako kontrakt

```text
ZLA definicja:
  revenue = amount
  → co to jest "amount"? per order? per item? brutto czy netto?

DOBRA definicja:
  revenue = SUM(quantity * unit_price)
  filtry:   status = 'paid', bez cancelled i refunded
  grain:    1 wiersz na klienta

CHECKI JAKOSCI:
  customer_id NOT NULL
  revenue >= 0
  COUNT = COUNT(DISTINCT customer_id)
```

<!-- end_slide -->

# Revenue: co sprawdzaja checki?

Te checki mowia:
- wynik ma wlasciciela,
- revenue nie jest ujemne,
- jest 1 wiersz na klienta.

<!-- end_slide -->

# Revenue: checki jakosci

```text
CHECKI JAKOSCI:
  check                              dlaczego?
  --------------------------------   --------------------------------
  tylko zamowienia paid              nie licz cancelled jako sprzedazy
  COUNT przed i po JOIN              wiesz czy JOIN zmienil grain
```

Metryka bez definicji, filtra statusu, grain i checkow jest tylko liczba.

<!-- end_slide -->

# CTE: bonus

CTE = `WITH` — nazwany krok wewnatrz query.

Bez CTE — wszystko w jednym bloku, trudno czytac:

```sql
SELECT customer_id, SUM(quantity * unit_price) AS revenue
FROM orders
JOIN order_items USING (order_id)
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(quantity * unit_price) > 0;
```

Im dluzsze query, tym trudniej zobaczyc co robi kazdy krok.

<!-- end_slide -->

# CTE: przyklad z WITH

```sql
WITH paid_orders AS (
    SELECT order_id, customer_id
    FROM orders
    WHERE status = 'paid'
),
line_revenue AS (
    SELECT order_id, quantity * unit_price AS line_value
    FROM order_items
)
SELECT customer_id, SUM(line_value) AS revenue
FROM paid_orders
JOIN line_revenue USING (order_id)
GROUP BY customer_id;
```

Wynik identyczny. Kazdy krok ma nazwe — latwiej czytac i debugowac.
CTE nie tworzy tabeli, istnieje tylko w tym query.

Performance: CTE na tym przykladzie nic nie zmienia.
Optimizer (SQLite, DuckDB, Postgres) wkleja CTE inline i wykonuje ten sam plan.
CTE to narzedzie czytelnosci, nie optymalizacji.

<!-- end_slide -->

# Walidacja wyniku

Minimalne checki:

```text
customer_id nie jest NULL
revenue >= 0
jeden wiersz na klienta
tylko zamowienia paid
wyjasniona liczba rekordow przed i po joinie
```

Bez walidacji mamy tylko nadzieje, nie pewny wynik.

<!-- end_slide -->

# Java → DE: analogia dla backendowca

```text
Java/backend          Data Engineering
--------------------  --------------------
kontrakt endpointu    kontrakt danych
DTO/encja             schemat/tabela
request id            order id
logika serwisu        logika transformacji
unit test             check walidacyjny SQL
konsument API         odbiorca danych
```

<!-- end_slide -->

# Zadania do pracy domowej

1. Obejrz dane i policz rekordy w 4 tabelach.
2. Policz query biznesowe: paid, statusy, revenue.
3. Zbuduj finalne query `customer_order_summary`.
4. Dopisz 4 proste validation checks.
5. Opisz grain tabel i finalnego wyniku.
6. Oddaj pliki `01_solution.sql` - `05_interview_answers.md`.

<!-- end_slide -->

# Praca domowa

Najpierw uruchom baze:

Na Windowsie: WSL Ubuntu, nie PowerShell.

```bash
cd student/lab
sqlite3 lesson_01.db < schema.sql
sqlite3 lesson_01.db < seed_data.sql
```

```text
schema.sql    = tworzy tabele
seed_data.sql = laduje gotowe dane
```

<!-- end_slide -->

# Praca domowa: pomocnicze laby

Potem uzyj cwiczen pomocniczych, jesli potrzebujesz prowadzenia krok po kroku:

```text
1. lab/04_sql_basics_extra_tasks.sql  -> zobaczenie danych
2. lab/02_join_revenue_tasks.sql      -> JOIN, revenue, summary
3. lab/03_modeling_workshop.md        -> grain i walidacje slowami
4. lab/01_ddl_dml_warmup.sql          -> opcjonalny DDL/DML warm-up
```

`teoria.md` jest krotka i konkretna.
Do minimum wystarczy.
Po lekcji poszerzaj SQL samodzielnie w internecie.

<!-- end_slide -->

# Praca domowa: doczytaj

Po lekcji doczytaj szczegolnie:
- `JOIN`,
- `GROUP BY`,
- grain,
- walidacje,
- CTE.

<!-- end_slide -->

# Praca domowa: finalny homework

Oddaj:

Oddajesz finalny homework:

Te pliki tworzysz samodzielnie:

```text
homework/lesson_01/
├── 01_solution.sql
├── 02_validation_checks.sql
├── 03_grain_map.md
├── 04_data_product_brief.md
└── 05_interview_answers.md
```

<!-- end_slide -->

# Praca domowa: laby i PR

Oddajesz tez rozwiazane laby:

```text
student/lab/04_sql_basics_extra_tasks.sql
student/lab/02_join_revenue_tasks.sql
student/lab/03_modeling_workshop.md
student/lab/01_ddl_dml_warmup.sql  # opcjonalnie
```

Nie oddajesz `student/lab/lesson_01.db`.

Prace oddajesz przez pull request na GitHubie.
Tam dostaniesz review i poprawki.

<!-- end_slide -->

# Pytanie na rozmowie

Pytanie na rozmowie:

```text
Co moze pojsc nie tak przy joinie orders i order_items?
```

<!-- end_slide -->