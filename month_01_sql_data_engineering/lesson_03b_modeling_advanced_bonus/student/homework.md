# Praca domowa bonusowa: Lekcja 03b

Ten homework jest opcjonalny.

## Cel

Masz pokazać, że rozumiesz zaawansowane pojęcia modelowania jako odpowiedzi na konkretne problemy.

To nie jest lista definicji do zapamiętania.

Punktem startowym jest prosty model z lekcji 03:

```text
dim_customer
dim_product
fact_sales
```

W bonusie pytasz: co się psuje, gdy model rośnie?

## Co Oddać

```text
homework/lesson_03b/
├── advanced_modeling_notes.md
└── mini_examples.sql
```

## Krok 1: notatka techniczna

W `advanced_modeling_notes.md` odpowiedz według schematu:

```text
Problem:
Jakie pojęcie rozwiązuje problem:
Mini-przykład:
Kiedy nie komplikować modelu:
```

Opisz te problemy:

1. Klient zmienia region.
   Wyjaśnij SCD Type 1 vs SCD Type 2 oraz business key vs surrogate key.

2. Dochodzą inne fact tables, np. zwroty i sprzedaż.
   Wyjaśnij conformed dimension na przykładzie `dim_date`.

3. Nie każdy fact opisuje to samo.
   Porównaj transaction fact, periodic snapshot fact i accumulating snapshot fact.

4. Nie każdą metrykę wolno sumować tak samo.
   Wyjaśnij additive, semi-additive i non-additive measure.

5. W fact table jest `order_id`, ale nie ma sensu robić osobnej tabeli `dim_order`.
   Wyjaśnij degenerate dimension.

6. Produkt ma wiele tagów, a jeden tag pasuje do wielu produktów.
   Wyjaśnij bridge table i pokaż ścieżkę joinu:

```text
fact_sales -> dim_product -> bridge_product_tag -> dim_tag
```

7. Dwa dashboardy liczą revenue inaczej.
   Wyjaśnij semantic layer i czym różni się od Gold table.

Każdy punkt: 3-5 zdań. Najpierw problem, potem nazwa pojęcia.

## Krok 2: mini-przykłady SQL

W `mini_examples.sql` pokaż 4 mini-przykłady na CTE:

1. `dim_customer_scd2` z `customer_sk`, `customer_id`, `valid_from` i `valid_to`.
   Dopisz komentarz, dlaczego `customer_id` nie wystarcza jako jedyny klucz.

2. `dim_date` jako conformed dimension używana przez dwa facty, np. `fact_sales_daily` i `fact_returns_daily`.
   Dopisz komentarz, dlaczego oba facty powinny mieć tę samą definicję daty.

3. Non-additive measure: pokaż, dlaczego `AVG(conversion_rate)` bywa złe i kiedy użyć `SUM(conversions) / SUM(visits)`.

4. Bridge table: pokaż `dim_product`, `dim_tag` i `bridge_product_tag`.
   Dopisz komentarz, dlaczego revenue może się podwoić, jeśli produkt ma kilka tagów.

To mogą być CTE z kilkoma rekordami. Nie musisz tworzyć pełnych tabel.

## Granica

Nie buduj produkcyjnego pipeline'u SCD, pełnej semantic layer ani dużego modelu tagów.

Ten bonus ma sprawdzić, czy umiesz rozpoznać problem i dobrać pojęcie.

## Checklista

- [ ] Wiem, kiedy business key nie wystarcza.
- [ ] Wiem, czym różni się SCD Type 1 od SCD Type 2.
- [ ] Wiem, po co jest surrogate key przy SCD Type 2.
- [ ] Wiem, po co wiele factów używa tej samej dimension.
- [ ] Wiem, że różne fact tables mają różny grain.
- [ ] Wiem, że nie każdą metrykę wolno po prostu sumować albo uśredniać.
- [ ] Wiem, kiedy `order_id` może zostać w fact table jako degenerate dimension.
- [ ] Wiem, jak bridge table łączy produkt z tagami.
- [ ] Wiem, że bridge table może podwoić metrykę po joinie.
- [ ] Wiem, że semantic layer centralizuje definicję metryk.
