# Lab: prosty model analityczny e-commerce

## Kontekst

Firma e-commerce chce analizować dzienną sprzedaż.

W tym labie skupiasz się na minimum, które trzeba dobrze zrozumieć:

- co jest faktem,
- co jest wymiarem,
- jaki jest grain tabeli,
- jak policzyć revenue,
- jak sprawdzić, czy Gold zgadza się z fact.

To nie jest zadanie o najdłuższy SQL. To jest zadanie o decyzje modelowania: use case, grain, warstwa, metryka, check.

## Dane Źródłowe

Dane źródłowe są blisko aplikacji:

```text
raw_customers
raw_products
raw_orders
raw_order_items
```

Traktujemy je jak lokalny odpowiednik Bronze.

Możesz je zobaczyć zwykłym SQL:

```sql
SELECT * FROM raw_orders ORDER BY order_id;
SELECT * FROM raw_order_items ORDER BY order_item_id;
```

Najważniejszy przykład do zapamiętania:

```text
order_id 100 ma status paid i dwie pozycje:
Keyboard: 1 * 120 = 120
Mouse:    2 * 80  = 160

Razem order 100 ma revenue 280, ale fact_sales ma dwa rekordy.
```

## Docelowy Przepływ

```text
raw_* tables
  -> dim_customer / dim_product / fact_sales
  -> gold_daily_sales
```

Jak czytać ten przepływ:

```text
Medallion:
  raw/Bronze -> cleaned model -> Gold

Kimball:
  dim_customer + dim_product + fact_sales

Star schema:
  fact_sales w centrum, dimensions dookoła

OLAP/dashboard:
  zapytania i wykresy typu revenue po dniu
```

To nie są osobne alternatywy. To są różne poziomy tej samej pracy.

```text
Medallion mówi: gdzie dane są w pipeline.
Kimball/star mówi: jak dane są ułożone do analizy.
OLAP mówi: jak użytkownik pyta o metryki po wymiarach.
```

## Decyzje Do Obrony

- `fact_sales` ma grain jednej pozycji opłaconego zamówienia.
- Revenue liczymy jako `quantity * unit_price`.
- Do paid revenue bierzemy tylko `status = 'paid'`.
- `dim_customer` daje opis klienta i region.
- `dim_product` daje opis produktu i kategorię.
- `gold_daily_sales` jest denormalizowanym Goldem pod dashboard dzienny.
- `gold_daily_sales` ma grain jednego dnia sprzedaży.

## Star Schema Vs Gold

Porównujesz dwa sposoby użycia danych:

```text
Wariant A: fact_sales + dim_customer + dim_product
Wariant B: gotowa tabela gold_daily_sales
```

Zapisz w notatce:

```text
Kiedy wybrałbym star schema:
Kiedy wybrałbym Gold:
Co jest łatwiejsze dla dashboardu:
Co jest bezpieczniejsze dla dalszej analizy:
```

Dotykalny test:

```sql
SELECT
  o.order_date,
  SUM(fs.line_revenue) AS total_revenue
FROM fact_sales AS fs
JOIN raw_orders AS o
  ON fs.order_id = o.order_id
GROUP BY o.order_date;
```

To samo pytanie może potem dostać gotowy Gold dzienny:

```sql
SELECT *
FROM gold_daily_sales;
```

Porównaj, co jest wygodniejsze dla dashboardu, a co elastyczniejsze dla analityka.

OLAP-owo oba warianty mogą odpowiedzieć na pytanie:

```text
Jakie revenue mamy po dniu?
```

Różnica jest praktyczna:

```text
Star schema: analityk może sam dobrać wymiary i robić joiny.
Gold: dashboard dostaje gotowy wynik dzienny.
```

Jeśli chcesz rozszerzyć lab, możesz później dodać Gold per region i kategorię. Nie jest to wymagane w pracy domowej.

## Netflix-Style Przykład

Wyobraź sobie platformę streamingową.

Najpierw jeden konkretny event:

```text
profile_7 obejrzał 600 sekund tytułu Stranger Things na TV.
```

```text
fact_watch_event: jeden rekord = jedno zdarzenie oglądania
dim_title: jeden rekord = jeden tytuł
dim_profile: jeden rekord = jeden profil użytkownika
gold_daily_title_watch_time: jeden rekord = dzień + tytuł
```

Pytanie kontrolne:

```text
Dlaczego nie wystarczy jedna tabela ze wszystkim: profile, title, device, watch_time, country, genre, plan?
```

Odpowiedź ma dotyczyć grainu, duplikacji i różnych use case'ów.

## Zadania Przed SQL

Zapisz krótko:

1. Co oznacza jeden rekord w każdej raw table?
2. Dlaczego `fact_sales` jest na poziomie order item, a nie order?
3. Dlaczego `cancelled` i `refunded` nie wchodzą do paid revenue?
4. Kiedy analityk powinien użyć fact/dim, a kiedy Gold?
5. Jakie checki pokazują, że model jest bezpieczny?

## Co Zapisać Po Labie

Do homeworku przenieś:

- projekt modelu do `model_design.md`,
- SQL do `transformations.sql`,
- checki do `quality_checks.sql`,
- krótką odpowiedź techniczną o fact, dimension i Gold do `model_design.md`.