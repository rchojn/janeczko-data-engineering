---
title: Lekcja 11 - Spark / PySpark Foundations
author: Data Engineering Course
date: 2026-09-04
---

# Lekcja 11

Spark / PySpark Foundations

```text
Kiedy dane są za duże na Polars?
Bronze → Silver transform na PySpark.
```

<!-- end_slide -->

# Problem biznesowy

Masz pipeline lokalny, działa, ale skala rośnie:

```text
2 GB -> 500 GB -> 5 TB
```

To nie jest problem jednej funkcji.
To jest problem architektury wykonania danych.

W praktyce: da się to zrobić lokalnie, ale nie da się robić to samo w sposób stabilny i powtarzalny przy dużej skali.

<!-- end_slide -->

# Dlaczego to jest ważne?

```text
Single node = memory + CPU + disk
Distributed engine = many executors + partitions + shuffle
```

Nie chodzi o to, żeby „używać Sparka”, tylko o to, żeby rozumieć, gdzie pojawiają się bottlenecki i kiedy jeden notebook przestaje być wystarczający.

<!-- end_slide -->

# Agenda

```text
1. Dlaczego Spark
2. Co to jest bronze/silver
3. Lazy evaluation i plan wykonania
4. PySpark DataFrame API
5. Partitioning i output quality
6. Najczęstsze błędy
7. Homework + interview
```

<!-- end_slide -->

# Learning goals

Po tej lekcji umiesz:

```text
wyjaśnić kiedy Spark ma sens,
odróżnić transformation vs action,
napisać prosty job Bronze -> Silver,
rozpoznać czy pipeline jest idempotentny,
uniknąć 4 typowych błędów początkujących.
```

<!-- end_slide -->

# First principles

```text
Jedna maszyna ma limit RAM.
Disk i network są dużo wolniejsze niż RAM.
```

Gdy dane przekraczają możliwości jednej maszyny:
- rośnie spill,
- rośnie time-to-result,
- rośnie ryzyko awarii jobu.

Spark dzieli pracę na wiele executorów i partycji.

<!-- end_slide -->

# Polars vs PySpark

```text
Polars  = single-node, bardzo szybki lokalnie
PySpark = distributed, skala klastra
```

Reguła praktyczna:

```text
start: Polars
scale: PySpark gdy dane nie mieszczą się w RAM jednej maszyny
```

<!-- end_slide -->

# Co to jest Spark

Spark to engine, który:

```text
czyta dane,
buduje plan,
optymalizuje plan,
wykonuje taski na partycjach,
zapisuje wynik.
```

Ty opisujesz transformacje.
Spark decyduje, jak je wykonać najskuteczniej.

<!-- end_slide -->

# Architektura

```text
Driver
  -> plan i koordynacja

Cluster Manager
  -> przydział zasobów

Executors
  -> faktyczna praca na danych
```

W praktyce: `driver` planuje, `executor` wykonuje.

<!-- end_slide -->

# Słownik 4 pojęć

```text
Job       = uruchomienie po action
Stage     = część joba między shuffle
Task      = praca na jednej partycji
Partition = logiczny fragment danych
```

To są podstawowe słowa do czytania `Spark UI` i `EXPLAIN`.

<!-- end_slide -->

# Bronze / Silver / Gold

```text
Bronze = raw input, bez "przycinania" biznesowego
Silver = cleaned + normalized + valid
Gold   = business-ready aggregates
```

Najpierw robisz poprawny raw import.
Potem zbierasz czystość danych.
Na końcu liczyć możesz metryki biznesowe.

<!-- end_slide -->

# SparkSession

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("OrdersPipeline")
    .master("local[*]")
    .getOrCreate()
)
```

Praktyka:
- jedna sesja na job,
- `getOrCreate()` zamiast ręcznego SparkContext.

<!-- end_slide -->

# Ingest Bronze

```python
df_bronze = (
    spark.read
    .option("inferSchema", "true")
    .json("data/bronze/orders/")
)
```

Bronze ma być minimalnie przetworzonym wejściem. Nie wolno mylić raw z "gotowym do raportów".

<!-- end_slide -->

# Lazy evaluation

```python
df1 = spark.read.json("data/orders.json")
df2 = df1.filter(df1.status == "completed")
df3 = df2.select("order_id", "total_amount")
```

Na tym etapie Spark jeszcze nie liczy. To dopiero plan wykonania.

<!-- end_slide -->

# Action uruchamia job

```python
df3.count()
df3.show(5)
df3.write.parquet("output/")
```

Dopiero `action` uruchamia obliczenia.
To bardzo ważne dla debugowania i performance.

<!-- end_slide -->

# Narrow vs wide

```text
Narrow: filter/select/withColumn
  -> zwykle bez shuffle

Wide: groupBy/join/distinct
  -> zwykle shuffle
```

Wide operacje są droższe i szybciej widzą się w `EXPLAIN`.

<!-- end_slide -->

# DataFrame API — dobre praktyki

```python
from pyspark.sql import functions as F

(df_bronze
    .withColumn("status", F.trim(F.lower(F.col("status"))))
    .withColumn("total_amount", F.col("total_amount").cast("double"))
    .filter(F.col("order_id").isNotNull()))
```

Widzisz tu dokładnie to, czego oczekujemy po `Silver`: standardyzacja i walidacja wejścia.

<!-- end_slide -->

# Partitioning

```python
df_silver.write \
    .mode("overwrite") \
    .partitionBy("status") \
    .parquet("output/silver/orders/")
```

Cel:
- mniejsze pliki do odczytu,
- faster pruning w query,
- lepsza organizacja danych wyjściowych.

<!-- end_slide -->

# Typowe pułapki

```text
1. collect() na dużym DataFrame
2. pętla Python po recordach
3. brak normalization statusu
4. zapis bez kontroli jakości wejścia
```

W Spark najczęściej winą jest nie `kod`, tylko `logika danych` i `niezrozumiały plan wykonania`.

<!-- end_slide -->

# Homework i interview

```text
Homework: napisz job Bronze -> Silver + 3 testy
Interview: pokaż, kiedy Spark ma sens, a kiedy nie
```

Najważniejsze pytanie:

```text
Czy to problem RAM, skali czy bezpieczeństwa danych?
```

<!-- end_slide -->
