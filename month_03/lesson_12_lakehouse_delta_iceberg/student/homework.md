# Praca domowa: Lekcja 12

## Cel

Masz pokazać, że rozumiesz różnicę pomiędzy "folderem z Parquetem" a "tabelą w lakehouse".

To nie jest tylko "zapisz DataFrame do Delta". To jest praktyka odpowiedzi na pytania:

```text
Co się stanie, gdy dwa joby zapisują do tego samego katalogu?
Jak wrócić do poprzedniej wersji danych?
Czy możemy dopisywać nowe kolumny bez przebudowy wszystkich rekordów?
```

<!-- end_slide -->

## Co i gdzie oddajesz

```text
homework/lesson_12/
├── delta_pipeline.py
├── schema_evolution_case.md
├── tests/
│   └── test_delta.py
├── output/
│   └── delta/
└── README.md
```

`student/lab/` jest do eksperymentu, `homework/lesson_12/` to finalny artefakt do review.

<!-- end_slide -->

## Problem biznesowy

Masz pipeline danych, który działa lokalnie: folder z Parquet, czasami kilka appendów, czasem rewrite, a potem pojawiają się problemy:

```text
- nadpisanie przez inny job,
- brak historii wersji danych,
- brak prostego rollback,
- trudność z dodaniem nowej kolumny bez psucia starego outputu.
```

To jest klasyczny moment, w którym pojawia się potrzeba tabeli lakehouse zamiast zwykłego katalogu plików.

<!-- end_slide -->

## Krok 1: przygotowanie środowiska

```bash
pip install pyspark==3.5.0 delta-spark==3.2.0
```

Następnie konfigurujesz sesję Spark z Delta extensions:

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

<!-- end_slide -->

## Krok 2: zapis do Delta

```python
ORDERS = [
    {"order_id": "1001", "status": "completed", "amount": 120.5},
    {"order_id": "1002", "status": "pending",   "amount":  80.0},
    {"order_id": "1003", "status": "completed", "amount": 240.0},
]

path = "output/delta/orders"
df = spark.createDataFrame(ORDERS)
df.write.format("delta").mode("overwrite").save(path)
```

To jest pierwszy z punktów: zapis jako Delta, nie zwykły Parquet.

<!-- end_slide -->

## Krok 3: append i historia zmian

Dodaj nowy batch:

```python
NEW_ORDERS = [
    {"order_id": "1004", "status": "completed", "amount": 200.0},
]

spark.createDataFrame(NEW_ORDERS).write.format("delta").mode("append").save(path)
```

Po tym kroku sprawdź historię:

```python
from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, path)
dt.history().select("version", "operation").show()
```

Zobaczysz, że każda operacja ma wersję commit. To jest bardzo ważny sygnał lakehouse: każda zmiana jest auditowalna.

<!-- end_slide -->

## Krok 4: time travel

Najpierw zrób wersję 0, potem bieżącą:

```python
v0 = spark.read.format("delta").option("versionAsOf", 0).load(path)
current = spark.read.format("delta").load(path)
```

Dodatkowo wypisz:

```text
v0_count = v0.count()
current_count = current.count()
print(f"v0: {v0_count} rekordów, current: {current_count} rekordów")
```

To daje prosty i mocny mechanizm rollbacku po błędnym update albo zlym appendzie.

<!-- end_slide -->

## Krok 5: schema evolution

Dodaj kolumnę `region` tylko do nowych rekordów:

```python
EU_ORDERS = [{"order_id": "1005", "status": "completed", "amount": 95.0, "region": "EU"}]

spark.createDataFrame(EU_ORDERS).write.format("delta").option("mergeSchema", "true").mode("append").save(path)
```

Wynik: stare rekordy mają `NULL` w `region`, a nowe rekordy mają `EU`. To jest właśnie `schema evolution`.

<!-- end_slide -->

## Krok 6: opis w markdown

Plik `schema_evolution_case.md` powinien odpowiedzieć na 3 pytania:

1. Kiedy potrzebujesz schema evolution zamiast przebudowy tabeli?
2. Co się dzieje bez `mergeSchema=true` gdy schema się zmienia?
3. Kiedy plain Parquet wystarczy, a kiedy potrzebujesz Delta?

Dobrą odpowiedź charakteryzuje to, że Delta daje kontrolę nad historycznym stanem tabeli, a nie tylko format pliku.

<!-- end_slide -->

## Krok 7: testy

Minimum 3 testy:

- `test_history_has_write_versions`
- `test_time_travel_returns_previous_state`
- `test_schema_evolution_adds_new_column`

To ma pokazać, że nie tylko zapisujesz do Delta, ale weryfikujesz zachowanie tabeli w produkcyjnym scenariuszu.

<!-- end_slide -->

## Acceptance criteria

- [ ] `python delta_pipeline.py` uruchamia się bez błędów
- [ ] `time travel` zwraca poprzednią wersję tabeli
- [ ] po `schema evolution` kolumna `region` jest dostępna dla nowych rekordów
- [ ] `history()` pokazuje kolejne wersje commitów
- [ ] `schema_evolution_case.md` odpowiada na 3 pytania z rozwagą
- [ ] testy przechodzą: `pytest tests/`

<!-- end_slide -->
