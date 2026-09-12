# Teoria: Lekcja 10 - Struktury danych w Pythonie

## ELI5

Struktura danych to pojemnik na dane.
W Pythonie masz rozne pojemniki i kazdy jest dobry do innego zadania:

- list: gdy kolejnosc ma znaczenie,
- tuple: gdy rekord ma byc staly,
- set: gdy chcesz unikalnosc,
- dict: gdy chcesz szybki lookup po kluczu.

## First Principles

Nie wybierasz struktury "bo tak".
Wybierasz pod operacje:

```text
append?               -> list
constant lookup?      -> dict / set
dedup?                -> set
grouping i counting?  -> dict
immutable key?        -> tuple
```

Najpierw pytasz: jaka operacja dominuje.
Potem dobierasz strukture, zeby koszt czasu i kodu byl sensowny.

## Mutability

Mutowalne:

- list,
- dict,
- set.

Niemutowalne:

- tuple.

To wplywa na bugi.
Jesli zmieniasz obiekt in-place i przekazujesz go dalej, latwo o side effects.

## list

Uzywaj, gdy:

- chcesz zachowac kolejnosc,
- przetwarzasz rekordy sekwencyjnie,
- budujesz wynik krok po kroku.

Nie uzywaj listy do szybkiego sprawdzania przynaleznosci dla duzych kolekcji.

## tuple

Uzywaj, gdy:

- chcesz stabilny, niemutowalny rekord,
- tworzysz klucz z wielu pol,
- chcesz hashable key do dict.

Przyklad ETL:

```text
key = (customer_id, order_date)
```

## set

Uzywaj, gdy:

- chcesz usunac duplikaty,
- chcesz szybko sprawdzic, czy element juz byl,
- budujesz filtry typu allowlist/denylist.

Klasyczny wzorzec ETL:

```text
seen_order_ids = set()
if order_id in seen_order_ids: skip
```

## dict

Uzywaj, gdy:

- chcesz mapowanie key -> value,
- robisz counting,
- robisz grouping,
- przechowujesz rekordy po ID.

Przyklad:

```text
revenue_by_customer[customer_id] += amount
```

## Zlozonosc operacji

Orientacyjnie:

- list membership: O(n),
- dict lookup: O(1) average,
- set membership: O(1) average.

To jest powod, dlaczego duze pipeline nie powinny robic lookupow na listach, gdy mozna uzyc dict/set.

## Socratic check

Pytanie: mam 5 mln order_id i chce sprawdzac duplikaty. list czy set?

Odpowiedz: set, bo membership jest srednio O(1), a dla list O(n).

Pytanie: mam payload order i chce quick access do total_amount. tuple czy dict?

Odpowiedz: dict, bo pola sa nazywane kluczami i latwo je czytac.

## Najczestsze bledy

1. Trzymanie wszystkiego w list i linear search wszedzie.
2. Uzywanie tuple tam, gdzie potrzeba mutacji.
3. Uzywanie set do danych, gdzie kolejnosc ma znaczenie.
4. Uzywanie mutable obiektu jako klucza dict.

## Closing check

Powiedz na glos:

```text
Dobieram strukture danych pod operacje i koszt,
a nie pod przyzwyczajenie.
```
