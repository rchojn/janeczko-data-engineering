# Praca domowa: Lekcja 10 - Struktury danych w Pythonie

## Cel

Masz pokazac, ze umiesz dobrac strukture danych do problemu ETL.
Nie chodzi o definicje z pamieci. Chodzi o decyzje inzynierskie.

Budzet pracy: okolo 10h.

## Co i gdzie robisz

```text
homework/lesson_10/
  data_structures_etl.py
  test_data_structures_etl.py
  notes.md
```

## Krok 0: ELI5 + First Principles

W `notes.md` zapisz:

1. ELI5: czym rozni sie list, tuple, set, dict.
2. First Principles: jak wybierasz strukture pod dominujaca operacje.
3. Socratic: dlaczego dedup na liscie jest slabszy niz na secie.

Bez tego nie przechodz do kodu.

## Krok 1: model danych i dedup

W `data_structures_etl.py` przygotuj funkcje:

- `deduplicate_orders(orders: list[dict[str, str]]) -> list[dict[str, str]]`
- dedup ma dzialac po `order_id` przez `set`.

## Krok 2: index po kluczu

Dodaj:

- `build_orders_index(orders: list[dict[str, str]]) -> dict[str, dict[str, str]]`
- klucz: `order_id`, wartosc: caly rekord.

## Krok 3: agregacja

Dodaj:

- `revenue_by_customer(orders: list[dict[str, str]]) -> dict[str, float]`
- licz tylko status `completed`.

## Krok 4: tuple jako klucz zlozony

Dodaj:

- `count_by_customer_day(orders: list[dict[str, str]]) -> dict[tuple[str, str], int]`
- klucz to `(customer_id, order_date)`.

## Krok 5: testy

Napisz minimum 8 testow:

1. dedup usuwa duplikaty po order_id,
2. index zwraca rekord po kluczu,
3. agregacja pomija non-completed,
4. tuple key dziala dla 2 klientow i 2 dni,
5. pusta lista nie wywala kodu,
6. brakujacy klucz jest obslugiwany sensownie,
7. parse kwoty dziala dla string,
8. wynik jest deterministic.

## Krok 6: notatka techniczna

W `notes.md` dopisz:

1. gdzie uzyles list,
2. gdzie uzyles set,
3. gdzie uzyles dict,
4. gdzie uzyles tuple,
5. dlaczego te decyzje sa sensowne.

## Definition of done

```text
[ ] Kod ma type hints.
[ ] Dedup jest przez set.
[ ] Lookup i agregacje sa przez dict.
[ ] Klucz zlozony jest tuple.
[ ] Testy przechodza lokalnie.
[ ] notes.md ma ELI5, First Principles i Socratic.
```
