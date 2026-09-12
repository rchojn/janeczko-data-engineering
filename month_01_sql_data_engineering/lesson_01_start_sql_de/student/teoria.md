# Teoria: Lekcja 01 - SQL i grain

Ten plik jest checklista do zrozumienia homeworku. Nie ucz sie definicji na pamiec. Po kazdej sekcji zadaj sobie pytanie: "czy umiem wyjasnic to na danych customers/orders/order_items/products?".

Minimum tej lekcji:

```text
1. Obejrzec dane.
2. Zrozumiec grain tabel.
3. Polaczyc tabele poprawnym JOIN-em.
4. Policzyc revenue = quantity * unit_price tylko dla zamowien paid.
5. Zrobic finalny wynik: jeden rekord na klienta.
6. Dodac proste checki walidacyjne.
```

CTE jest dodatkiem. Nie jest wymagane w podstawowym homeworku.

<!-- end_slide -->

## 1. Model mentalny

Przed trudniejszym query odpowiedz na 4 pytania:

```text
1. Z jakich tabel biore dane?
2. Co oznacza jeden rekord w kazdej tabeli?
3. Co ma oznaczac jeden rekord w wyniku?
4. Jak sprawdze, ze wynik nie jest przypadkowo zly?
```

Jesli nie umiesz odpowiedziec na pytanie 2 albo 3, zatrzymaj sie przed pisaniem SQL.

<!-- end_slide -->

## 2. Dataset

Pracujemy na malym sklepie:

```text
customers    = klienci
orders       = zamowienia
order_items  = pozycje zamowien
products     = produkty
```

Najwazniejsze relacje:

```text
customers.customer_id -> orders.customer_id
orders.order_id       -> order_items.order_id
products.product_id   -> order_items.product_id
```

<!-- end_slide -->

## 3. Grain

Grain oznacza: co znaczy jeden rekord.

```text
customers              jeden rekord = jeden klient
orders                 jeden rekord = jedno zamowienie
order_items            jeden rekord = jedna pozycja zamowienia
products               jeden rekord = jeden produkt
customer_order_summary jeden rekord = jeden klient
```

Dlaczego to wazne: po JOIN-ie `orders -> order_items` jedno zamowienie moze pojawic sie kilka razy, bo jedno zamowienie moze miec kilka produktow.

<!-- end_slide -->

## 4. DDL vs DML

DDL zmienia strukture tabeli:

```sql
CREATE TABLE test_orders (...);
ALTER TABLE test_orders ADD COLUMN source_file TEXT;
DROP TABLE IF EXISTS test_orders;
```

DML czyta albo zmienia dane:

```sql
SELECT * FROM orders;
INSERT INTO test_orders VALUES (...);
UPDATE test_orders SET load_status = 'processed';
```

W tej lekcji DDL/DML cwicz tylko na tabeli testowej. Nie zmieniaj tabel `customers`, `orders`, `order_items`, `products`.

<!-- end_slide -->

## 5. SELECT i filtrowanie

Zaczynaj od malych query:

```sql
SELECT *
FROM customers;

SELECT
    customer_id,
    customer_name,
    email
FROM customers;

SELECT *
FROM orders
WHERE status = 'paid';

SELECT *
FROM orders
ORDER BY order_date DESC
LIMIT 3;
```

`WHERE` filtruje pojedyncze rekordy przed agregacja.

<!-- end_slide -->

## 6. JOIN

`JOIN` laczy tabele po kluczach.

```sql
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.status
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

`JOIN` pokazuje tylko rekordy z dopasowaniem po obu stronach.

`LEFT JOIN` zostawia wszystkie rekordy z lewej tabeli, nawet jesli po prawej stronie nie ma dopasowania. Uzyj go, gdy finalny raport ma pokazac tez klientow bez zamowien paid.

<!-- end_slide -->

## 7. GROUP BY i HAVING

`GROUP BY` zwija wiele rekordow do jednej grupy.

```sql
SELECT
    status,
    COUNT(*) AS orders_count
FROM orders
GROUP BY status;
```

`HAVING` filtruje grupy po agregacji:

```sql
SELECT
    status,
    COUNT(*) AS orders_count
FROM orders
GROUP BY status
HAVING COUNT(*) > 1;
```

Zapamietaj:

```text
WHERE  = filtr przed GROUP BY
HAVING = filtr po GROUP BY
```

<!-- end_slide -->

## 8. Revenue

W tej lekcji revenue/przychod liczymy z `order_items`:

```text
revenue = quantity * unit_price
paid revenue = revenue tylko dla orders.status = 'paid'
```

Nie uzywaj samego `SUM(unit_price)`, bo ignoruje liczbe sztuk (`quantity`).

<!-- end_slide -->

## 9. Kolejnosc logiczna SQL

SQL piszesz od `SELECT`, ale baza logicznie mysli tak:

```text
FROM / JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

Dwa czeste bledy:

```text
1. Alias z SELECT uzyty w WHERE.
   Problem: WHERE dzieje sie przed SELECT.

2. COUNT(*) > 1 w WHERE.
   Problem: COUNT(*) powstaje dopiero po GROUP BY, wiec filtr grupy idzie do HAVING.
```

<!-- end_slide -->

## 10. Walidacja

Query, ktore zwraca wynik, jeszcze nie musi byc poprawne biznesowo.

Minimalne checki do homeworku:

```text
1. Czy customers.customer_id jest unikalny?
2. Czy orders.order_id jest unikalny?
3. Czy quantity w order_items jest dodatnie?
4. Ile rekordow jest w orders przed i po joinie z order_items?
```

Najwazniejsze pytanie po finalnym query:

```text
Czy naprawde mam jeden rekord na klienta?
```

<!-- end_slide -->

## 11. CTE

To jest bonus.

CTE znaczy Common Table Expression. W SQL piszesz je przez `WITH`.

Najprosciej: CTE to nazwany krok wewnatrz jednego query. Nie tworzy stalej tabeli w bazie. Dziala tylko dla tego jednego zapytania, w ktorym go zapiszesz.

Po co sie go stosuje: zeby rozbic dlugie query na czytelne kroki. Zamiast pisac wszystko naraz, mozesz najpierw nazwac `paid_orders`, potem `order_revenue`, a na koncu zrobic finalny SELECT.

Minimalny ksztalt:

```sql
WITH paid_orders AS (
    SELECT *
    FROM orders
    WHERE status = 'paid'
)
SELECT *
FROM paid_orders;
```

Nie uzywaj CTE w minimum tylko po to, zeby query wygladalo profesjonalnie. Najpierw zrob prosty `JOIN`, `WHERE`, `GROUP BY` i walidacje.

<!-- end_slide -->

## Checklista przed oddaniem

- [ ] Umiem powiedziec, co oznacza jeden rekord w kazdej tabeli.
- [ ] Wiem, ktory JOIN moze zwiekszyc liczbe rekordow.
- [ ] Revenue licze jako `quantity * unit_price`.
- [ ] Revenue licze tylko dla zamowien `paid`.
- [ ] Finalny wynik ma jeden rekord na klienta.
- [ ] Mam 4 proste checki walidacyjne.
