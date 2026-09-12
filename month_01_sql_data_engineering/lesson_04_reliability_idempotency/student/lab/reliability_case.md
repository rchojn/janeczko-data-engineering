# Lab: niezawodny pipeline zmian zamowien

## Kontekst

System zrodlowy nie wysyla codziennie pelnej tabeli zamowien. Wysyla zmiany:

- `INSERT`,
- `UPDATE`,
- `DELETE`.

Kazda zmiana trafia do `bronze_order_changes`.

## Problem

Source czasem wysyla ten sam event dwa razy. Dodatkowo jedno `order_id` moze miec wiele zmian.

To oznacza:

```text
Bronze != current orders
```

Bronze jest dziennikiem zmian. Silver ma byc aktualnym stanem zamowien.

Najwazniejsze pytanie labu:

```text
Co stanie sie, jesli ten sam pipeline uruchomimy drugi raz?
```

## Jak pracowac aktywnie

Nie zakladaj, ze pipeline jest dobry, bo SQL sie odpala. Przy kazdym kroku zapisz gwarancje:

```text
Krok:
Jaki input przyjmuje:
Jaki output tworzy:
Co stanie sie przy retry:
Jaki check wykryje blad:
```

Lab jest zaliczony dopiero wtedy, gdy umiesz wskazac, gdzie chronisz sie przed duplicate event, gdzie wybierasz current state i gdzie usuwasz `DELETE` z Gold.

## Docelowy przeplyw

```text
bronze_order_changes
  -> deduped_order_changes
  -> current_order_state
  -> silver_orders
  -> gold_daily_sales
```

## Wazne przypadki w seed data

- `chg_002` wystepuje dwa razy.
- `order_id = 1001` ma `INSERT`, potem `UPDATE` do `paid`.
- `order_id = 1002` finalnie ma `refunded`.
- `order_id = 1003` finalnie ma `DELETE`.
- `order_id = 1004` ma old `order_date`, ale late `change_timestamp`.

## Zadania przed SQL

Zapisz odpowiedzi w `homework/lesson_04/pipeline_runs_design.md` albo w roboczej notatce:

1. Co jest grain Bronze?
2. Co jest grain Silver?
3. Po czym deduplikujesz duplicate event?
4. Po czym wybierasz najnowszy stan zamowienia?
5. Czy `DELETE` powinien wejsc do Gold?
6. Jak retry moglby podwoic revenue?
7. Dlaczego Gold budujemy z Silver, a nie prosto z Bronze?

## Zadania SQL

W [in_class_tasks.sql](in_class_tasks.sql) zbudujesz kolejne kroki. Przy kazdym kroku dopisz w komentarzu:

```text
Klucz:
Grain:
Co moze pojsc zle przy retry:
Jaki check to wykrywa:
```

## Zadanie dodatkowe: symulacja retry

Opisz, co powinno sie stac, jesli ten sam input z `bronze_order_changes` zostanie przetworzony drugi raz.

W `pipeline_runs_design.md` dopisz:

```text
Co mogloby sie podwoic w naiwnym pipeline:
Ktory krok w moim projekcie temu zapobiega:
Jaki check wykryje podwojenie:
Jaki komunikat wpisalbym do runbooka:
```

## Zadanie dodatkowe: late data

`order_id = 1004` ma stary `order_date`, ale pozny `change_timestamp`.

Odpowiedz:

```text
Ktora data decyduje o partycji biznesowej Gold:
Ktora data decyduje o tym, kiedy pipeline zobaczyl zmiane:
Czy trzeba przeliczyc starszy dzien:
Jak duzy lookback window wybralbym na start i dlaczego:
```

## Co zapisac po labie

Do [../homework.md](../homework.md) przenies:

- logike loadu do `reliable_load.sql`,
- metadata uruchomien do `pipeline_runs_design.md`,
- checki do `validation_checks.sql`,
- symulacje retry i late data do `pipeline_runs_design.md`,
- plan reakcji na blad do `incident_runbook.md`.