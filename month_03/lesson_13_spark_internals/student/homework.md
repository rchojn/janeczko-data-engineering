# Praca domowa: Lekcja 13 - Spark Internals

## Cel

Masz pokazac, ze umiesz diagnozowac wolny Spark job zamiast stroic go na slepo.
To nie jest tylko lekcja o PySpark.
To jest lekcja o kosztach execution planu.

## Co i gdzie robisz

Pracujesz w dwoch miejscach:

```text
student/lab/
  spark_internals_demo.py      -> aktywne demo i zrodlo obserwacji

homework/lesson_13/
  01_explain_walkthrough.md
  02_join_strategy_benchmark.py
  03_skew_investigation.md
  04_skew_fix.py
  05_runtime_tuning_notes.md
  06_interview_answers.md
```

Jak o tym myslec:

```text
student/lab/        = eksperyment i obserwacja
homework/lesson_13/ = finalna odpowiedz do review
```

## Szacowany budzet pracy

```text
1.0h  powtorka: job / stage / task / partition
2.0h  uruchomienie labu i analiza Spark UI
2.0h  benchmark join strategy
2.0h  skew investigation + fix
1.5h  tuning notes i explain walkthrough
1.5h  interview answers i self-review
```

## Krok 0: uruchom demo

```bash
python student/lab/spark_internals_demo.py
```

W trakcie pracy odpowiedz na 4 pytania:

```text
Gdzie jest shuffle?
Ktory task/stage jest najdrozszy?
Czy widze skew?
Czy broadcast albo cache daje realny efekt?
```

## Krok 1: `01_explain_walkthrough.md`

W tym pliku opisz jeden konkretny plan:

1. jaki DataFrame analizujesz,
2. gdzie pojawia sie `Exchange`,
3. czy widzisz `BroadcastHashJoin` albo `SortMergeJoin`,
4. jaki to daje koszt,
5. co zmienilbys jako pierwszy.

Nie wklejaj samego outputu. Zinterpretuj go.

## Krok 2: `02_join_strategy_benchmark.py`

Napisz skrypt porownujacy:

1. join bez broadcast,
2. join z `F.broadcast()`,
3. ten sam join z roznymi `spark.sql.shuffle.partitions`.

Wypisz:

- wynik `explain(mode="formatted")`,
- czas wykonania,
- krotki wniosek: kiedy broadcast ma sens, a kiedy nie.

## Krok 3: `03_skew_investigation.md`

Na podstawie danych skewed opisz:

1. ktory klucz dominuje,
2. jak widac to w `groupBy().count()`,
3. jak widac to w Spark UI,
4. dlaczego problem nie znika tylko dlatego, ze cluster ma wiecej workerow.

Wazne: odpowiedz wprost, czym rozni sie "duzo danych" od "zly rozklad danych".

## Krok 4: `04_skew_fix.py`

Zaimplementuj prosty fix skew przez salting.

Masz pokazac:

1. wersje bez fixu,
2. wersje z saltingiem,
3. komentarz, dlaczego ten fix pomaga,
4. komentarz, kiedy w realnej pracy najpierw probowalbys AQE zamiast recznego salting.

## Krok 5: `05_runtime_tuning_notes.md`

Opisz 5 decyzji wykonaniowych:

1. kiedy zmieniasz `shuffle.partitions`,
2. kiedy wlaczasz / zostawiasz AQE,
3. kiedy cache ma sens,
4. kiedy problemem jest write layout i small files,
5. kiedy nie dotykasz configu, tylko zmieniasz plan danych.

Dla kazdego punktu dopisz:

```text
Symptom:
Pierwszy check:
Mozliwy fix:
Ryzyko fixu:
```

## Krok 6: `06_interview_answers.md`

Odpowiedz na pytania:

1. Co to jest shuffle i dlaczego jest drogi?
2. Kiedy broadcast join jest lepszy od sort-merge join?
3. Co to jest data skew i jak je wykrywasz?
4. Czym rozni sie repartition od coalesce?
5. Kiedy cache pomaga, a kiedy szkodzi?

## Definition of done

Praca jest gotowa, gdy umiesz pokazac:

1. jeden plan z `Exchange` i jego interpretacje,
2. jeden sensowny benchmark broadcast vs shuffle,
3. jeden przypadek skew i jego fix,
4. jedna decyzje tuningowa uzasadniona objawem, a nie zgadywaniem.
