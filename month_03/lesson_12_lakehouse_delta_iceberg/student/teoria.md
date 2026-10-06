# Teoria: Lakehouse — Delta Lake / Iceberg

Ten plik ma pokazać, dlaczego zwykły Parquet nie wystarcza w produkcji i kiedy potrzebujesz tabeli lakehouse.

## Minimum tej lekcji

```text
1. Wiesz, co robi zwykły Parquet i gdzie ma limit.
2. Rozumiesz, co oznacza ACID w danych lakehouse.
3. Potrafisz wyjaśnić time travel i schema evolution.
4. Wiesz, kiedy Delta Lake ma sens, a kiedy zwykły Parquet jest wystarczający.
5. Rozumiesz, że lakehouse to nie tylko format, ale też commit log, historia i integracja z pipeline.
```

Jeśli nie potrafisz wytłumaczyć, co robi `Delta` w 2 zdaniach, to nie zrozumiałeś jeszcze problemu, który rozwiązujemy.

<!-- end_slide -->

## 1. Model mentalny

Zanim zaczniesz mówić o Delta, zadaj sobie 4 pytania:

```text
1. Czy zapis do tabeli ma być atomic?
2. Czy trzeba wrócić do poprzedniej wersji danych?
3. Czy schema może się zmieniać z czasem?
4. Czy kilka jobów może pisać do tej samej tabeli jednocześnie?
```

Jeśli odpowiedź na którekolwiek z tych pytań to „tak”, to zwykły Parquet jest za słaby.

### Prosty przykład biznesowy

```text
Zamówienia są zapisane jako Parquet.
Pipelines zapisuje nową wersję danych.
Pewnego dnia job wywołuje overwrite z błędnym filtrem.
Zniknęły dane, nie ma historii, nie da się wrócić.
```

W Delta taki przypadek jest mniej katastrofalny: masz `history()`, `time travel` i `transaction log`.

<!-- end_slide -->

## 2. ELI5

Plain Parquet to jak folder z plikami. Dobrze czyta się dane, ale:

- nie da się łatwo zaktualizować jednego rekordu,
- zapis jest mniej bezpieczny przy równoczesnym pisaniu,
- nie wiadomo, jak dane wyglądały wczoraj albo tydzień temu,
- łatwo uszkodzić dane przez złe overwrite.

Delta Lake to "Parquet + commit log + historia + transakcje".

```text
Plain Parquet: szybki odczyt, ale brak ACID, brak historii
Delta Lake:    Parquet + _delta_log + commit history = ACID + time travel + schema evolution
```

To jest kluczowa różnica: Delta nie jest „magiczny format”, tylko dobrze ułożony system danych na plikach Parquet.

<!-- end_slide -->

## 3. Problem z plain Parquet

### Partial write

```text
Pipeline zapisuje 10 partycji.
Pada po 7.
Dane są niekompletne.
Kolejny read widzi 7 partycji zamiast 10.
```

Brak transakcji = brak atomowości.

### Concurrent writes

```text
Job A i Job B zapisują do tego samego katalogu.
Oba robią mode("overwrite").
Job B nadpisuje pliki, których Job A jeszcze nie zatwierdził.
```

Wynik: uszkodzone dane, trudne do debugowania.

### Brak historii

```text
Bug w pipeline nadpisał 3 miliony rekordów błędnymi wartościami.
Parquet: nie ma poprzedniej wersji.
Delta: versionAsOf = 5 -> wróć do wersji przed bugiem.
```

To jest najważniejszy biznesowy argument do Delta.

<!-- end_slide -->

## 4. Jak działa Delta Lake

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

`_delta_log/` = transaction log.

Każda operacja jest zapisywana jako commit log, a pliki danych pozostają niezmieniane w miejscu. To pozwala na:

- atomic write,
- rollback,
- usuwanie konfliktów przy równoczesnym zapisie,
- historię i metadane.

## ACID w praktyce

```text
Atomicity:    cały write albo nic
Consistency:  schema jest sprawdzane przed zapisem
Isolation:    konflikty między jobami są wykrywane
Durability:   commit log jest trwały i bezpieczny
```

W praktyce: to jest to, czego brakuje zwykłemu Parquet i co krytycznie pomaga w produkcji.

<!-- end_slide -->

## 5. Time Travel

```python
# wersja 0 — zanim dodano nowe dane
spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("data/delta/orders")

# wersja z konkretnego czasu
spark.read.format("delta") \
    .option("timestampAsOf", "2026-09-01 12:00:00") \
    .load("data/delta/orders")
```

Zastosowania:

- debugowanie błędu w pipeline,
- powrót do wcześniejszej wersji danych,
- audyt i analiza zmian,
- odpowiedź na pytanie „co się stało wczoraj?”

W biznesie to jest bardzo ważne, bo nie ma sensu „tego nie da się przywrócić”, jeśli tabela ma historię.

<!-- end_slide -->

## 6. Schema evolution

```python
new_df = df.withColumn("region", F.lit("EU"))

new_df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save("data/delta/orders")
```

W praktyce:

- stare rekordy mają `NULL` w kolumnie `region`,
- nowe rekordy mają wartość `EU`,
- tabela się rozwija bez pełnej przebudowy.

Bez `mergeSchema` sparks zgłasza błąd schematu. A to jest bardzo typowy problem przy zmianach kolumn w pipeline.

<!-- end_slide -->

## 7. Parquet vs Delta vs Iceberg

| Cecha | Plain Parquet | Delta Lake | Iceberg |
|-------|---------------|------------|---------|
| ACID | ✗ | ✅ | ✅ |
| Time travel | ✗ | ✅ | ✅ |
| Schema evolution | manual | ✅ | ✅ |
| Update/delete per row | ✗ | ✅ | ✅ |
| Spark-native | ✅ | ✅ | ✅ |
| Databricks preference | zależnie | ✅ | ✓ |
| Multi-engine | ✅ | mocno Spark | ✅ |

### Dobre zasady decyzji

```text
Zwykły Parquet = gdy dane są tylko odczytywane i nie zmieniają się często.
Delta Lake = gdy chcesz bezpieczeństwo, historię i łatwy rollback.
Iceberg = gdy chcesz multi-engine i silniejszy model tabeli w ekosystemie.
```

<!-- end_slide -->

## 8. Socratic questions

```text
- Czy bez historii można łatwo zdebugować błąd w pipeline?
- Czy overwrite bez transakcji może wymazać dane?
- Czy schema zmienia się w czasie w realnym systemie?
- Czy jedna tabela może być zapisywana przez kilka jobów jednocześnie?
- Czy przychodzi Ci do głowy scenariusz, w którym plain Parquet byłby niebezpieczny?
```

Jeżeli potrafisz odpowiedzieć „tak” na co najmniej trzy z tych pytań i wyjaśnić dlaczego, to zrozumiałeś sens lakehouse.

<!-- end_slide -->

## 9. STAŁY PATTERN — zapamiętaj to

```text
DELTA LAKE — stały wzorzec

=== Konfiguracja SparkSession z Delta ===
from delta import configure_spark_with_delta_pip
builder = SparkSession.builder \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()

=== Zapis ===
df.write.format("delta").mode("overwrite").save("path/delta/table")

=== Odczyt ===
spark.read.format("delta").load("path/delta/table")

=== Time travel ===
spark.read.format("delta").option("versionAsOf", 0).load(path)

=== Schema evolution ===
df.write.format("delta").option("mergeSchema", "true").mode("append").save(path)

=== Historia ===
from delta.tables import DeltaTable
dt = DeltaTable.forPath(spark, path)
dt.history().show()

CHECKLIST:
[ ] configure_spark_with_delta_pip()
[ ] mode("overwrite") albo mode("append") jest jawny
[ ] mergeSchema przy zmianie schema
[ ] history() do audytu
[ ] versionAsOf do rollback
```

## 10. Checkpoint: czy to naprawdę działa w głowie?

```text
1. Czy wiesz, co jest problemem z plain Parquet?
2. Czy potrafisz wytłumaczyć, po co jest `_delta_log`?
3. Czy potrafisz wyjaśnić time travel nie używając słowa „magia”?
4. Czy potrafisz powiedzieć, kiedy Delta jest lepszy od Parquet w realnym pipeline?
```

Jeśli tak — masz zasadniczy zmysł lakehouse. Nie musisz pamiętać wszystkich opcji, ale musisz wiedzieć, po co one są.

<!-- end_slide -->
