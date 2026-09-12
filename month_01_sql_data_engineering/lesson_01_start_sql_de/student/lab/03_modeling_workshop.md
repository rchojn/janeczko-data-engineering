# Cwiczenie pomocnicze: grain, ryzyka i walidacje

Cel: zrozumiec, co oznaczaja rekordy w tabelach i jaki ma byc wynik finalny.

To jest brudnopis do homeworku. Nie oddajesz tego pliku; przenosisz wnioski do `homework/lesson_01/`.

Pracujesz na tabelach z [schema.sql](schema.sql): `customers`, `orders`, `order_items`, `products`.

Jak pisac odpowiedzi:

- krotko, po 1-3 zdania na punkt,
- konkretnie na danych z tej lekcji,
- bez definicji z internetu.

Ten plik pomaga glownie w `03_grain_map.md`, `04_data_product_brief.md` i `05_interview_answers.md`.

<!-- end_slide -->

## Zadanie 1: okresl grain

Dla kazdej tabeli dokoncz zdanie:

- `customers`: jeden rekord oznacza...
- `orders`: jeden rekord oznacza...
- `order_items`: jeden rekord oznacza...
- `products`: jeden rekord oznacza...

<!-- end_slide -->

## Zadanie 2: zaprojektuj finalny wynik

Chcemy przygotowac tabele `customer_order_summary` dla analityka biznesowego.

Odpowiedz:

- jaki powinien byc grain tej tabeli?
- jakie kolumny powinny sie w niej znalezc?
- czy uwzgledniamy anulowane zamowienia?
- co robimy z klientami bez zamowien?
- co robimy z klientami bez zamowien paid?

<!-- end_slide -->

## Zadanie 3: ryzyka

Wymien minimum 3 rzeczy, ktore moga pojsc zle przy budowie tej tabeli.

Podpowiedz: mysl o joinach, anulowanych zamowieniach, klientach bez zamowien, duplikatach i definicji revenue/przychodu.

<!-- end_slide -->

## Zadanie 4: walidacje

Zaproponuj minimum 3 checki walidacyjne dla `customer_order_summary`.

Nie musza byc idealne. Maja pokazac, jak sprawdzisz, czy wynik ma sens.

Przyklad formatu:

```text
Nazwa checka:
Dlaczego ma znaczenie:
Pomysl SQL:
```

<!-- end_slide -->

## Opcjonalnie: test brzegowy

Zaproponuj trzy dodatkowe rekordy testowe, ktore moglyby zepsuc `customer_order_summary`:

```text
1. Klient bez zamowien -> ktore query go zgubi?
2. Zamowienie bez order_items -> co stanie sie z revenue/przychodem?
3. Produkt nigdy niekupiony -> czy LEFT JOIN nadal go pokazuje?
```

Nie musisz od razu modyfikowac `seed_data.sql`, ale musisz opisac, jaki wynik powinien sie zmienic.

<!-- end_slide -->

## Opcjonalnie: przeglad wlasnego query

Wybierz jedno query i napisz mini-przeglad:

```text
Cel query:
Grain wejscia:
Grain wyniku:
Join, ktory moze zwiekszyc liczbe rekordow:
Check, ktory wykryje blad:
Jedna rzecz, ktora poprawilbym przed oddaniem:
```

<!-- end_slide -->

## Co przeniesc do homeworku

Do [../homework.md](../homework.md) przenies:

- grain map do `03_grain_map.md`,
- decyzje o finalnym wyniku do `04_data_product_brief.md`,
- checki do `02_validation_checks.sql`,
- pytania niejasne do notatek albo przegladu z mentorem.
