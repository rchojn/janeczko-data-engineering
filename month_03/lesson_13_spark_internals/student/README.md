# Dla uczestnika: Lekcja 13 - Spark Internals, shuffle, skew i koszt wykonania

## Otworz i zrob to

1. Uruchom [lab/spark_internals_demo.py](lab/spark_internals_demo.py).
2. Otworz Spark UI na `http://localhost:4040` i znajdz najdrozszy stage.
3. Przeczytaj [teoria.md](teoria.md) i odpowiedz glosno na pytania kontrolne.
4. Wroc do [patterns.md](patterns.md) po kazdym demie.
5. Finalna prace zapisz w `homework/lesson_13/` wedlug [homework.md](homework.md).

Najkrotsza zasada folderow:

```text
student/lab/        = aktywne demo i miejsce diagnostyki
homework/lesson_13/ = finalne artefakty do review
```

Ta lekcja ma dawac wyraznie wiecej niz month_02.
W month_02 pisales Python i pipeline logic.
Tutaj uczysz sie, dlaczego ten sam kod zaczyna kosztowac 10x wiecej po wzroscie danych.

## Cel lekcji

Po tej lekcji masz umiec powiedziec:

- co to jest `job`, `stage`, `task`, `partition`,
- czym rozni sie narrow transformation od wide transformation,
- gdzie powstaje `shuffle` i dlaczego jest drogi,
- jak wykryc `skew`,
- kiedy uzyc `broadcast join`,
- kiedy `cache` pomaga, a kiedy tylko zuzywa memory,
- jak czytac `explain()` i Spark UI zamiast zgadywac.

## Jak uruchomic lab

```bash
python student/lab/spark_internals_demo.py
```

Spark UI:

```text
http://localhost:4040
```

Patrz szczegolnie na:

- DAG Visualization,
- SQL / Jobs,
- Stages,
- task duration outliers,
- shuffle read / shuffle write.

## Najwazniejszy kontrakt tej lekcji

Przy kazdym wolnym jobie odpowiedz najpierw:

```text
Gdzie jest shuffle?
Czy jest skew?
Czy join strategy ma sens?
Czy problem jest logiczny czy fizyczny?
```

Jesli nie umiesz odpowiedziec, nie zaczynaj strojenia na slepo.

## Materialy rekomendowane

1. Apache Spark Tuning Guide
   https://spark.apache.org/docs/latest/tuning.html

2. Databricks tutorial: Build an ETL pipeline with Apache Spark on the Databricks platform
   https://docs.databricks.com/aws/en/getting-started/etl-quick-start

3. Spark SQL performance tuning overview
   https://spark.apache.org/docs/latest/sql-performance-tuning.html

Te materialy sa po to, zeby polaczyc lokalne demo z realnym cluster thinking.
Nie czytaj wszystkiego naraz. Wybierz jeden temat: shuffle, skew albo broadcast.
