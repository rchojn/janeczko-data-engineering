# Lab case: wolny Spark pipeline

## Kontekst

Masz pipeline:

```text
orders_raw
  -> join customers
  -> groupBy country, order_date
  -> revenue report
```

Dziala poprawnie dla malych danych.
Po wzroscie wolumenu runtime rosnie duzo szybciej niz biznes akceptuje.

## Pytanie lekcji

```text
Czy problem jest w logice,
czy w fizycznym planie wykonania?
```

## Co masz sprawdzic

1. Czy join robi shuffle?
2. Czy lookup table kwalifikuje sie do broadcast?
3. Czy klucz ma skew?
4. Czy liczba partycji ma sens?
5. Czy output write nie robi za wielu plikow?
6. Czy cache jest uzasadniony?

## Kontrakt pracy

Przy kazdym eksperymencie zapisz:

```text
Objaw:
Pierwszy check:
Dowod z planu lub UI:
Hipoteza:
Fix:
Ryzyko fixu:
```

## Kiedy lab jest zaliczony

1. Umiesz wskazac jeden konkretny `Exchange` w planie.
2. Umiesz pokazac jeden przypadek skew.
3. Umiesz obronic jeden broadcast join i jeden przypadek, gdy broadcast nie ma sensu.
4. Umiesz odroznic tuning configu od zmiany danych albo planu.
