---
title: Lekcja 12 - Lakehouse / Delta Lake / Iceberg
author: Data Engineering Course
date: 2026-09-03
---

# Lekcja 12

Lakehouse / Delta Lake / Iceberg

```text
Od plików do tabeli z historią, ACID i rollbackiem.
```

<!-- end_slide -->

# Agenda

```text
1. Problem z plain Parquet
2. Czym jest lakehouse
3. Delta Lake: commit log + ACID
4. Time travel i rollback
5. Schema evolution
6. Delta vs Iceberg
7. Różnica między plikami a tabelą
8. Lab + checklist
```

<!-- end_slide -->

# Problem biznesowy

Masz pipeline, który zapisuje dane do katalogu z Parquetem.

```text
raw/orders/
  part-0001.parquet
  part-0002.parquet
  part-0003.parquet
```

To działa, dopóki:
- jest jeden writer,
- jest mało jobów,
- nie trzeba wrócić do poprzedniego stanu,
- nie zmienia się schema.

Rzeczywistość jest inna:

```text
partial write
concurrent writes
bad overwrite
brak historii
brak audytu
```

<!-- end_slide -->

# Co psuje się w plain Parquet?

### 1. Partial write

```text
Job zapisuje 10 partycji.
Po 7 padł proces.
Czytający widzi 7 plików, nie 10.
```

Dane są niekompletne. Każdy kolejny job widzi "częściowy stan".

### 2. Concurrent writes

```text
Job A i Job B robią overwrite do tego samego katalogu.
Jedna operacja nadpisuje drugą.
```

### 3. Brak rollbacku

```text
Bug zmienia 3M rekordów.
Nie ma poprzedniej wersji.
Dane są stracone.
```

<!-- end_slide -->

# Dlaczego to jest ważne?

```text
Parquet = format pliku
Delta = tabela + historia + transakcje
```

Dane w produkcji to nie tylko pliki. To stan systemu.

Jeśli tabela może być nadpisana przez kilka jobów, to potrzebujemy:
- atomowości,
- historii zapisów,
- walidacji schematu,
- możliwości powrotu do wersji sprzed błędu.

<!-- end_slide -->

# First principles

```text
Co to jest tabela danych?
```

Tabela to nie folder z plikami.
Tabela to:
- nazwa,
- schemat,
- stan danych,
- historia zmian,
- semantyka operacji na danych.

Parquet daje pliki. Delta daje tabelę z metadanymi i logiem transakcji.

<!-- end_slide -->

# Plain Parquet vs Lakehouse

```text
Plain Parquet
  -> katalog z plikami
  -> brak semantyki tabeli
  -> brak historii
  -> trudny rollback

Lakehouse / Delta
  -> tabela z commit logiem
  -> ACID semantics
  -> time travel
  -> schema evolution
```

To nie jest kosmetyka. To zmienia sposób, w jaki działają pipeline'y.

<!-- end_slide -->

# Czym jest lakehouse?

Lakehouse łączy dwie rzeczy:

```text
1. obejmowanie danych w data lake (s3 / ADLS / lokalny filesystem)
2. semantykę tabeli jak w warehouse (schema, transakcje, wersje)
```

Czyli:
- przechowujemy surowe dane w formacie open,
- ale zachowujemy kontrolę nad stanem i integracją tabeli.

Przykład:

```text
bronze/     -> surowe dane
silver/     -> oczyszczone dane
gold/       -> agregacje biznesowe
```

Delta jest jednym z najważniejszych formatów lakehouse.

<!-- end_slide -->

# Jak wygląda Delta na dysku?

```text
data/delta/orders/
├── _delta_log/
│   ├── 00000000000000000000.json
│   ├── 00000000000000000001.json
│   └── 00000000000000000002.json
├── part-00000-abc.parquet
├── part-00001-def.parquet
└── part-00002-ghi.parquet
```

`_delta_log` = transaction log.

To jest klucz do zrozumienia:
- Dane są w Parquet,
- ale metadane o zmianach są w logu Delta.

<!-- end_slide -->

# Co robi `_delta_log`?

```text
Każdy zapis jest traktowany jako commit.
Delta zapisuje:
- wersję tabeli,
- operację,
- schemat,
- pozycję nowych plików,
- informacje o zmianach.
```

To pozwala na:
- atomic zapis,
- zgodność przy równoczesnym zapisie,
- odczyt starej wersji,
- monitorowanie historii operacji.

<!-- end_slide -->

# ACID w praktyce

```text
Atomicity    = cały zapis albo nic
Consistency  = stan musi być spójny
Isolation    = konflikty między jobami są wykrywane
Durability   = log commit jest trwały
```

Przykład:

```text
Pipeline zapisuje 1000 rekordów.
Po 700 przestaje działać.
Delta nie zostawia częściowego stanu.
```

To jest różnica między "zapisem na pliki" a "stanem tabeli".

<!-- end_slide -->

# Dlaczego ACID ważne dla danych?

W raportach, warehouse i BI nie wolno mieć sytuacji:

```text
- czesciowo zapisanych danych,
- uszkodzonego stanu po overwrite,
- dat z różnym poziomem jakości,
- niejasnego pochodzenia błędu.
```

ACID nie jest akademickie. To jest narzędzie do:
- bezpieczeństwa danych,
- zrozumienia produkcji,
- utrzymania poprawności procesu ETL.

<!-- end_slide -->

# Time travel

Najważniejsza rzecz w Delta poza ACID: historia danych.

```python
spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("data/delta/orders")
```

Możesz odczytać:
- wcześniejszą wersję tabeli,
- stan z konkretnego czasu,
- wersję przed błędnym deployem.

```python
spark.read.format("delta") \
    .option("timestampAsOf", "2026-09-01 12:00:00") \
    .load("data/delta/orders")
```

<!-- end_slide -->

# Time travel — kiedy to pomaga?

```text
- błąd w pipeline wymazał 2 miliony rekordów
- deploy nadpisał dane wygenerowane w nocy
- trzeba sprawdzić, co było w ubiegły poniedziałek
- trzeba wykonać rollback bez rebuildu całego storage
```

To jest bardzo ważne w produkcji.

Business answer:

```text
"Nie mamy już danych?"
"Tak mamy — w wersji 3, zanim błąd się pojawił."
```

<!-- end_slide -->

# Historia operacji

```python
from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, "data/delta/orders")

dt.history().select("version", "timestamp", "operation").show()
```

`history()` pokazuje:
- która wersja była zapisana,
- kiedy,
- jaki typ operacji został wykonany,
- czy to był append, overwrite, merge, vacuum itd.

To jest audyt i podstawowy narzędziowy mechanizm dla platformy.

<!-- end_slide -->

# Schema evolution

W realnych danych schema się zmienia.

```python
new_df = df.withColumn("region", F.lit("EU"))

new_df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save("data/delta/orders")
```

Co dzieje się po dodaniu kolumny?
- nowe rekordy mają region,
- stare rekordy mają NULL,
- tabela nie pęka od razu,
- można świadomie rozbudować schema.

Bez `mergeSchema` Spark zgłasza błąd.

<!-- end_slide -->

# Schema drift — real problem

```text
Tydzień temu tabela miała: order_id, total_amount
Dziś pojawia się: order_id, total_amount, region, status_reason
```

To nie jest błąd. To normalny drift danych.

Wielkie dane = zmieniają się kolumny, source'y, payloady i KAFKA.

W Delta można to kontrolować. W plain Parquet jest to często "manual repair".

<!-- end_slide -->

# Jak skonfigurować Spark do Delta?

```python
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

spark = (
    configure_spark_with_delta_pip(
        SparkSession.builder
        .appName("DeltaLakeDemo")
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    .getOrCreate()
)
```

Ważne: nie chodzi tylko o `format("delta")`.
Trzeba też dodać rozszerzenie Spark i katalog Delta.

<!-- end_slide -->

# Zapis i odczyt w praktyce

```python
df.write.format("delta").mode("overwrite").save("data/delta/orders")

orders = spark.read.format("delta").load("data/delta/orders")
```

Zwykłe `read` i `write` działają, ale w Delta:
- zapis ma log transakcyjny,
- odczyt może odwoływać się do wersji,
- historia jest dostępna na poziomie tabeli.

<!-- end_slide -->

# Delta vs Iceberg

```text
Delta Lake
  -> mocne w Spark / Databricks / Azure
  -> silne wsparcie dla time travel + schema evolution

Apache Iceberg
  -> bardziej neutralny format tabeli w wielu silnikach
  -> mocny w ekosystemie AWS / Trino / Flink / Spark
```

### Kiedy co wybrać?

```text
Databricks / Azure / Spark-native      -> Delta Lake
AWS + Athena / Glue + multi-engine      -> Iceberg
```

Nie chodzi o to, który jest "najlepszy", tylko który jest naturalny dla platformy.

<!-- end_slide -->

# Delta vs Parquet — prosty kontrast

```text
Parquet
  -> szybki odczyt
  -> prosty format pliku
  -> brak historii
  -> brak transakcji
  -> łatwe overwrite bugi

Delta
  -> Parquet + commit log + historia
  -> ACID na plikach
  -> snapshot history
  -> schema evolution
```

Krótkie zdanie do zapamiętania:

```text
Delta nie jest "lepszy Parquet" jako plik.
Delta jest lepszą tabelą na danych lakehouse.
```

<!-- end_slide -->

# Data lake vs warehouse

```text
Warehouse: tabela ma semantykę, transakcje i kontrolę
Lake: dane są elastyczne, tańsze, lecz mniej „tabelowe"
Lakehouse: łączy oba modele
```

Lakehouse daje:
- przechowywanie w open format,
- skalowalność Data Lake,
- kontrolę tabeli jak w warehouse.

To jest najważniejsza architektura w nowoczesnych platformach danych.

<!-- end_slide -->

# Jak to wygląda w pipeline?

```text
bronze/*      -> surowe dane, bez wzorcowania
silver/*      -> czyste dane, walidacja i normalizacja
gold/*        -> agregacje biznesowe dla raportów
```

Delta wchodzi głównie w warstwy silver/gold, bo tam:
- trzeba mieć poprawne versioning,
- trzeba kontrolować schema,
- trzeba wracać po błędach,
- trzeba dawać spójne źródło dla raportów.

<!-- end_slide -->

# Warto zapamiętać

```text
DELTA LAKE — stały wzorzec

=== SparkSession ===
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

spark = configure_spark_with_delta_pip(
    SparkSession.builder
    .appName("DeltaDemo")
    .master("local[*]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
).getOrCreate()

=== Zapis ===
df.write.format("delta").mode("overwrite").save("data/delta/orders")

=== Odczyt ===
spark.read.format("delta").load("data/delta/orders")

=== Time travel ===
spark.read.format("delta").option("versionAsOf", 0).load("data/delta/orders")

=== Schema evolution ===
new_df.write.format("delta").option("mergeSchema", "true").mode("append").save("data/delta/orders")

=== Historia ===
from delta.tables import DeltaTable
DeltaTable.forPath(spark, "data/delta/orders").history().show()
```

<!-- end_slide -->

# Checklist przed labem

```text
[ ] Potrafię wyjaśnić, czym jest plain Parquet i gdzie ma limit
[ ] Potrafię powiedzieć, po co jest _delta_log
[ ] Potrafię wyjaśnić time travel bez magic phrases
[ ] Potrafię nazwać 3 scenariusze, gdzie Delta jest lepszy niż Parquet
[ ] Potrafię rozróżnić Delta i Iceberg
[ ] Potrafię zapisać prostą tabelę Delta i odczytać poprzednią wersję
```

Jeśli choć 4 z 6 punktów są jasne, to lekcja jest zrozumiała na poziomie praktycznym.

<!-- end_slide -->

# Homework / interview

## Pytanie 1

```text
Dlaczego plain Parquet nie wystarcza w produkcji?
```

## Pytanie 2

```text
Czym różni się Delta od zwykłego folderu danych?
```

## Pytanie 3

```text
Kiedy użyjesz `versionAsOf` albo `history()`?
```

## Pytanie 4

```text
Dlaczego `mergeSchema` ma sens przy ewolucji danych?
```

<!-- end_slide -->

# Podsumowanie

```text
Delta Lake nie jest „nowa ekstencja pliku”.
To jest nowy model pracy z danymi:
- tabele mają stan,
- mają historię,
- mają walidację i rollback,
- dają bezpieczniejszy pipeline.
```

To jest fundament, który pozwala przejść od "pliki na dysku" do "produkcyjnej platformy danych".

<!-- end_slide -->

# Homework i interview

```text
Homework: build Delta pipeline + time travel + schema evolution
Interview: explain why raw files are not enough in production
```

Najważniejsze pytanie:

```text
Czy Twoje dane są tylko plikami, czy są też wersjonowaną tabelą?
```

<!-- end_slide -->
