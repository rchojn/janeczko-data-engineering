# Praca domowa: Lekcja 03

## Cel

Masz zbudować prosty model analityczny sprzedaży i pokazać, że umiesz podjąć kilka decyzji modelarskich:

```text
raw data -> cleaned data -> fact/dim -> Gold
```

Najważniejsze są cztery rzeczy:

1. umiesz powiedzieć, jaki jest grain tabeli,
2. umiesz odróżnić fact od dimension,
3. umiesz sprawdzić, czy revenue liczy się poprawnie,
4. umiesz wyjaśnić, kiedy lepszy jest star schema, a kiedy gotowy Gold.

## Krok 0: przygotuj bazę

W katalogu `student/lab/` uruchom:

```bash
sqlite3 lesson_03.db < schema.sql
sqlite3 lesson_03.db < seed_data.sql
sqlite3 lesson_03.db
```

Przygotuj cztery pliki do oddania:

```bash
mkdir -p homework/lesson_03
touch homework/lesson_03/model_design.md
touch homework/lesson_03/transformations.sql
touch homework/lesson_03/quality_checks.sql
touch homework/lesson_03/interview_answer.md
```

## Krok 1: projekt modelu

W `model_design.md` odpowiedz krótko:

```text
Use case: jakie pytanie biznesowe chcę obsłużyć?
Odbiorca: kto będzie używał wyniku?
Grain fact_sales: jeden rekord = co?
Grain gold_daily_sales: jeden rekord = co?
Revenue: jak liczę metrykę?
Dimension tables: które tabele opisują kontekst?
Gold table: jaka tabela jest gotowa pod dashboard?
Data contract: kto jest odbiorcą, jaka jest oficjalna metryka, jakie checki blokują publikację?
```

Nie pisz długiego eseju. Wystarczy 1-3 zdania przy każdym punkcie.

## Krok 2: transformacje SQL

W `transformations.sql` zbuduj minimum 7 widoków:

1. `silver_customers`,
2. `silver_products`,
3. `silver_orders`,
4. `dim_customer`,
5. `dim_product`,
6. `fact_sales` tylko dla zamówień ze statusem `paid`,
7. `gold_daily_sales`.

Przed każdym `CREATE VIEW` dopisz krótki komentarz:

```text
-- Grain: jeden rekord = ...
-- Purpose: do czego służy ta tabela
```

W `fact_sales` revenue policz tak:

```text
line_revenue = quantity * unit_price
```

Silver views nie muszą robić dużej transformacji.

Wystarczy, że nazwiesz krok oczyszczania i zastosujesz proste reguły,
np. `LOWER(TRIM(...))` dla tekstu albo jawny wybór kolumn zamiast `SELECT *`.

## Krok 2b: trochę bardziej analityczny Gold

Dopisz dodatkowy widok:

```text
gold_sales_by_region_category
```

Grain tej tabeli:

```text
jeden rekord = jeden dzień + region klienta + kategoria produktu
```

Widok ma pokazać:

```text
order_date
region
category
total_revenue
order_count
line_count
```

To jest celowo bardziej zaawansowane niż `gold_daily_sales`.

Wymaga świadomego użycia fact table + dimensions i pilnowania grainu po joinach.

## Krok 2c: star schema query vs Gold query

W `transformations.sql` dopisz dwa SELECT-y porównawcze:

1. query z `fact_sales` + `dim_customer` + `dim_product`, które liczy revenue per `region` i `category`,
2. query z `gold_sales_by_region_category`, które odpowiada na podobne pytanie prościej.

Przed nimi dopisz komentarz:

```text
-- Trade-off: star schema jest bardziej elastyczny, Gold jest prostszy dla dashboardu.
```

## Krok 3: quality checks

W `quality_checks.sql` dodaj minimum 4 checki:

1. czy `dim_customer` nie ma duplikatów `customer_id`,
2. czy `dim_product` nie ma duplikatów `product_id`,
3. czy `fact_sales` nie ma pustych kluczy,
4. czy suma revenue z `fact_sales` zgadza się z `gold_daily_sales`.

Dopisz też minimum 3 dodatkowe checki:

5. czy `fact_sales` nie zawiera statusów innych niż `paid`,
6. czy `line_revenue` nigdy nie jest ujemne,
7. czy suma revenue z `fact_sales` zgadza się z `gold_sales_by_region_category`.

Każdy check może być zwykłym zapytaniem SQL, które powinno zwrócić 0 wierszy albo jedną wartość kontrolną.

## Krok 4: mini-decyzja o historii wymiaru

Na końcu `model_design.md` dopisz krótką sekcję:

```text
Co powinno się stać, jeśli klient zmieni region albo produkt zmieni kategorię?
Czy raport ma używać aktualnego opisu klienta/produktu?
Czy raport historyczny ma używać opisu z dnia sprzedaży?
```

Nie implementuj jeszcze historii wymiaru w SQL.

Chodzi o decyzję projektową: czy historyczne revenue ma być raportowane według starego kontekstu z dnia sprzedaży,
czy według aktualnego kontekstu klienta/produktu.

## Krok 5: krótka odpowiedź techniczna

W `interview_answer.md` odpowiedz na pytania:

```text
Czym różni się fact table od dimension table i po co budujemy Gold table?
Kiedy użyłbym star schema, a kiedy gotowego Golda?
Co to jest grain i dlaczego błąd grainu psuje revenue?
Co zrobiłbym, jeśli wymiar zmienia się w czasie?
```

Odpowiedź: 8-12 zdań łącznie, tak jakbyś tłumaczył to na review technicznym.

## Bonus 03b: SCD Type 2

SCD jest przeniesione do bonusu 03b, bo wymaga dodatkowych pojęć:
business key, surrogate key i zakres obowiązywania rekordu.

Ten bonus nie jest wymagany do zaliczenia lekcji 03.

Jeśli chcesz zobaczyć, jak wygląda historia wymiaru w SQL,
zrób [Bonus 03b](../../lesson_03b_modeling_advanced_bonus/student/README.md).

## Co oddać

Oddajesz:

```text
homework/lesson_03/
├── model_design.md
├── transformations.sql
├── quality_checks.sql
└── interview_answer.md
```

Nie oddajesz `student/lab/lesson_03.db`.

## Checklista przed oddaniem

- [ ] `fact_sales` ma grain jednej pozycji opłaconego zamówienia.
- [ ] `gold_daily_sales` ma grain jednego dnia sprzedaży.
- [ ] Revenue jest liczone jako `quantity * unit_price`.
- [ ] Dimensions opisują kontekst, np. klienta i produkt.
- [ ] Gold jest gotowy pod prosty dashboard dzienny.
- [ ] `gold_sales_by_region_category` ma grain dnia + regionu + kategorii.
- [ ] `quality_checks.sql` porównuje revenue z fact i Gold.
- [ ] `model_design.md` zawiera mini-decyzję: aktualny opis czy historia wymiaru.
- [ ] `interview_answer.md` tłumaczy star schema vs Gold.