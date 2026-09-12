---
title: Lekcja 10 - Struktury danych w Pythonie
author: Data Engineering Course
date: 2026-09-12
---

# Lekcja 10

Struktury danych w Pythonie

```text
list, tuple, set, dict
```

Cel: umiec wybrac dobra strukture do konkretnej operacji ETL.

<!-- end_slide -->

# TL;DR

Ta lekcja nie jest o teorii dla teorii.
To jest lekcja o decyzjach, ktore maja skutki w runtime.

```text
operacja -> koszt -> struktura danych
```

Jesli wybierzesz zla strukture, kod moze byc poprawny logicznie,
ale bedzie wolny, trudny w review i podatny na bugi.

<!-- end_slide -->

# Agenda

```text
1. Problem ETL i gdzie tracimy czas
2. list, tuple, set, dict w praktyce
3. Jeden case: dedup + lookup + agregacja
4. Anti-patterny i jak je naprawic
5. Checklista decyzji przed oddaniem homeworku
```

<!-- end_slide -->

# Problem biznesowy

Masz surowe orders z API.
Chcesz policzyc revenue per customer i oddac stabilny artefakt.

```text
musisz usunac duplikaty
musisz szybko sprawdzac rekordy po ID
musisz policzyc agregacje
musisz utrzymac czytelny kod i testy
```

Jedna struktura nie obsluzy wszystkiego dobrze.

<!-- end_slide -->

# Dane wejsciowe

```text
orders = [
  {"order_id": "1001", "customer_id": "C1", "status": "completed", "total_amount": "120.5"},
  {"order_id": "1002", "customer_id": "C1", "status": "pending",   "total_amount": "80.0"},
  {"order_id": "1001", "customer_id": "C1", "status": "completed", "total_amount": "120.5"}
]
```

To jest typowy payload: slowniki, duplikaty, stringowe kwoty.

<!-- end_slide -->

# list: kiedy uzywac

list jest dobra, gdy:

- liczy sie kolejnosc,
- idziesz rekord po rekordzie,
- budujesz wynik etapami.

To jest naturalna struktura dla sekwencji accepted records.

<!-- end_slide -->

# list: gdzie boli

Nie uzywaj listy jako glownej struktury do lookupow.

```text
if order_id in processed_ids_list
```

To oznacza linear search.
Przy duzych danych taki kod zwykle jest glownym powodem spowolnienia.

<!-- end_slide -->

# tuple: po co istnieje

tuple jest po to, zeby miec stabilny, niemutowalny klucz.

Przyklad:

```text
(customer_id, order_date)
```

Taki klucz dobrze dziala w dict przy grupowaniu po wielu polach.

<!-- end_slide -->

# tuple: praktyczny pattern

```python
count_by_customer_day: dict[tuple[str, str], int] = {}
key = (customer_id, order_date)
count_by_customer_day[key] = count_by_customer_day.get(key, 0) + 1
```

To jest prosty i czytelny sposob na composite grain.

<!-- end_slide -->

# set: kiedy jest najlepszy

set wybierasz, gdy potrzebujesz:

- unikalnosci,
- szybkiego membership check,
- deduplikacji po ID.

W ETL to jedna z najczesciej uzywanych struktur.

<!-- end_slide -->

# set: dedup w praktyce

```python
seen_ids: set[str] = set()
accepted: list[dict[str, str]] = []

for order in orders:
    order_id = order.get("order_id", "")
    if order_id in seen_ids:
        continue
    seen_ids.add(order_id)
    accepted.append(order)
```

Tu list i set pracuja razem: list trzyma kolejnosc, set pilnuje unikalnosci.

<!-- end_slide -->

# dict: kiedy jest najlepszy

dict wybierasz, gdy robisz:

- lookup po kluczu,
- counting,
- grouping,
- mapowanie key -> value.

W Python ETL dict jest glowna struktura dla indeksow i agregacji.

<!-- end_slide -->

# dict: agregacja revenue

```python
revenue_by_customer: dict[str, float] = {}

for order in accepted:
    if order.get("status", "").lower() != "completed":
        continue
    customer_id = order["customer_id"]
    amount = float(order["total_amount"])
    revenue_by_customer[customer_id] = revenue_by_customer.get(customer_id, 0.0) + amount
```

Ta logika jest prosta do review i prosta do testowania.

<!-- end_slide -->

# Zlozonosc i koszt

```text
list membership: O(n)
set membership: O(1) average
dict lookup: O(1) average
```

Interpretacja praktyczna:

- kilka rekordow: roznica mala,
- miliony rekordow: roznica krytyczna.

<!-- end_slide -->

# Myslowy benchmark

Masz 5 000 000 order_id i sprawdzasz duplikaty.

```text
list -> wiele porownan na kazdy rekord, koszt rosnie szybko
set  -> szybkie sprawdzenie, koszt rośnie znacznie wolniej
```

Nie chodzi o idealna formule. Chodzi o intuicje kosztu.

<!-- end_slide -->

# Anti-pattern 1

Wszystko jako list.

Objaw:

```text
lokalnie dziala,
na wiekszym batchu pipeline mocno zwalnia
```

Naprawa:

- dedup i membership do set,
- lookup i agregacje do dict.

<!-- end_slide -->

# Anti-pattern 2

set tam, gdzie musi byc kolejnosc biznesowa.

Objaw:

```text
niestabilny porzadek wynikow,
trudne porownanie outputow miedzy runami
```

Naprawa:

- sekwencje trzymaj w list,
- set uzywaj tylko jako pomocniczy indeks unikalnosci.

<!-- end_slide -->

# Anti-pattern 3

Nieplanowana mutacja rekordow.

Objaw:

```text
jeden etap zmienia dane,
kolejny etap dostaje nieoczekiwany stan,
testy przechodza tylko czasami
```

Naprawa:

- ogranicz mutacje,
- jawnie nazywaj etapy,
- testuj edge case i puste dane.

<!-- end_slide -->

# Decision flow

```text
Czy potrzebuje kolejnosci?
  tak -> list
  nie -> dalej

Czy potrzebuje unikalnosci lub membership?
  tak -> set
  nie -> dalej

Czy potrzebuje mapowania key -> value?
  tak -> dict
  nie -> dalej

Czy potrzebuje immutable composite key?
  tak -> tuple
```

<!-- end_slide -->

# Recipe ETL

```text
1. Przyjmij input jako list rekordow.
2. Zdefiniuj klucz dedup i trzymaj seen_ids w set.
3. Accepted records trzymaj w list.
4. Agregacje i index trzymaj w dict.
5. Gdy grupujesz po wielu polach, uzyj tuple key.
6. Dodaj testy: puste dane, duplikaty, brakujace pola.
```

<!-- end_slide -->

# Pytania na code review

1. Dlaczego tu jest list, a nie set?
2. Dlaczego dedup robisz przez set?
3. Gdzie jest granica mutacji danych?
4. Czemu ten klucz jest tuple?
5. Jak testem udowadniasz poprawna decyzje?

<!-- end_slide -->

# Co oddajesz

```text
homework/lesson_10/
  data_structures_etl.py
  test_data_structures_etl.py
  notes.md
```

W notes.md:

- ELI5,
- First Principles,
- odpowiedz Socratic,
- uzasadnienie wyboru struktur.

<!-- end_slide -->

# Definition of done

- [ ] dedup po order_id jest przez set
- [ ] lookup i agregacje sa przez dict
- [ ] klucz zlozony jest tuple
- [ ] list sluzy do uporzadkowanej iteracji
- [ ] testy pokrywaja edge case
- [ ] decyzje sa obronione na glos

<!-- end_slide -->

# Closing check

Pytanie:

```text
Masz 5 mln order_id i chcesz wykryc duplikaty.
list czy set i dlaczego?
```

Poprawna odpowiedz:

```text
set, bo membership check jest srednio O(1),
a list robi linear search O(n).
```
