# Teoria: Spark / PySpark Foundations

Ten plik jest checklistą do zrozumienia lekcji. Nie uczysz się „na pamięć”, tylko sprawdzasz, czy potrafisz wyjaśnić mechanikę Spark na prostym przykładzie orders/customers.

## Minimum tej lekcji

```text
1. Zrozum, co jest Driver, Executor, Partition i Task.
2. Zrozum różnicę między transformacją a action.
3. Zobacz, jak wygląda Bronze -> Silver pipeline.
4. Potrafisz wyjaśnić, dlaczego Spark ma sens przy dużych danych.
5. Umiesz dodać `withColumn`, `filter`, `groupBy` i `write` w praktyce.
```

Jeśli nie umiesz wyjaśnić tego na prostym przykładzie `orders`, nie przechodzisz dalej. To jest ten sam model, co w SQL: najpierw rozumienie danych, potem query, potem optymalizacja.

<!-- end_slide -->

## 1. Model mentalny

Przed trudniejszym jobem zadaj sobie 4 proste pytania:

```text
1. Co jest wejściem do joba?
2. Co jest grain jednego rekordu?
3. Co jest outputem finalnym?
4. Co może wyjść niepoprawnie przy surowych danych?
```

W Spark to jest bardzo ważne, bo łatwo rozegrać cały job i mieć wynik „ładny”, ale zły biznesowo.

Przykład:

```text
Wejście: surowe JSON z zamówieniami
Grain: jeden rekord = jedno zamówienie
Output: tabela Silver z normalizacją statusów i wartości
Ryzyko: `status` ma duże litery, `order_id` może być null, `total_amount` może być string
```

Wskazówka: jeżeli nie potrafisz opisać `grain`, nie zaczynaj pisać `groupBy` ani `join`.

<!-- end_slide -->

## 2. ELI5

Polars przetwarza dane na jednej maszynie — tyle ile masz RAM.

Spark dzieli dane na kawałki (partycje) i przetwarza je równolegle na wielu maszynach albo wątkach.

```text
Polars:  1 maszyna, 32 GB RAM → limit 32 GB danych
Spark:   10 maszyn × 32 GB   → limit 320 GB, można dodawać maszyny
```

To nie znaczy, że Spark jest „lepszy zawsze”. Ma koszt: startup, cluster, scheduling, shuffle, I/O. Dla małych danych Polars jest zwykle prostszy i szybszy.

## Kiedy Spark, kiedy Polars

| Kryterium | Polars | PySpark |
|-----------|--------|---------|
| Dane < 100 GB | ✅ | ✗ overhead |
| Dane > 100 GB | ✗ | ✅ |
| Lokalny prototyp | ✅ | ✗ |
| Klaster / Databricks | ✗ | ✅ |
| Wymagany produkt | zależy | często tak |

Praktyczna zasada: **zacznij od Polars lub prostego Python, przejdź na Spark, gdy dane nie mieszczą się w pamięci lub wątek tylko na jednej maszynie nie wystarcza**.

<!-- end_slide -->

## 3. First Principles: jak Spark przetwarza dane

```text
1. Driver program     — Twój kod Python. Plans the job, creates SparkSession.
2. Cluster Manager    — przydziela zasoby (YARN, Kubernetes, Standalone)
3. Executors          — procesy na węzłach, które czytają i transformują dane
4. Partitions         — dane są podzielone na kawałki i rozłożone po executorach
5. Tasks              — jedna jednostka pracy wykonywana na jednej partycji
```

Klucz: **driver tylko planuje, executors wykonują**.

To jest ważne, bo wiele błędów w Spark pochodzi z nieporozumienia: to nie jest jeden wielki Python, tylko rozproszony plan pracy.

<!-- end_slide -->

## 4. Lazy Evaluation — dlaczego Spark nie liczy od razu

```python
df = spark.read.json("data/orders.json")       # tylko plan odczytu
df2 = df.filter(df.status == "completed")      # tylko plan transformacji
df3 = df2.select("order_id", "total_amount")   # dalej plan, nic nie robi

# Dopiero action uruchamia job:
df3.show()
df3.count()
df3.write.parquet("output/")
```

`filter`, `withColumn`, `select`, `join` = transformacje.
`show`, `count`, `collect`, `write` = action.

Dlaczego to ma sens:

- Spark może zoptymalizować plan,
- może zbierać operacje razem,
- może odroczyć wykonanie do momentu, w którym naprawdę potrzebny jest wynik.

To zasadnicza różnica między „piszę kod” a „wykonuję job”.

<!-- end_slide -->

## 5. DataFrame API — to samo myślenie, inna składnia

```python
# POLARS
# filtr, normalizacja, agregacja
df.filter(pl.col("status") == "completed")
df.with_columns(pl.col("status").str.to_lowercase())
df.group_by("status").agg(pl.sum("total_amount"))

# PYSPARK
from pyspark.sql import functions as F

df.filter(F.col("status") == "completed")
df.withColumn("status", F.lower(F.col("status")))
df.groupBy("status").agg(F.sum("total_amount"))
```

To samo logiczne myślenie: clean → normalize → group → output. Jedyna różnica to konkretne API i środowisko wykonania.

<!-- end_slide -->

## 6. Partitioning — czemu ma znaczenie

Partycja = jeden kawałek danych, który trafia do jednego executora.

```python
# sprawdź liczbę partycji
df.rdd.getNumPartitions()

# zwiększ liczbę partycji
df.repartition(8)

# zmniejsz liczbę partycji bez shuffle
df.coalesce(1)
```

W praktyce:

```python
df.write.partitionBy("status").parquet("output/orders/")
```

To tworzy foldery typu:

```text
output/orders/status=completed/part-0000.parquet
output/orders/status=pending/part-0000.parquet
```

To nazywa się partition pruning. Jeśli filtrujesz po `status`, Spark czyta tylko odpowiedni folder, a nie cały zbiór.

Wskazówka: partycjonowanie ma sens tylko wtedy, gdy kolumna ma sensowną kardynalność i nie jest tak rozproszona, że tworzy miliony małych folderów.

<!-- end_slide -->

## 7. Socratic questions

Zamiast „czy to działa?”, pytaj:

```text
- Czy Spark ma sens dla tego rozmiaru danych?
- Czy układ partycji jest równomierny?
- Czy transformacje są naprawdę potrzebne, czy tylko źle zrobione?
- Czy outputem ma być pojedyncza tabela, czy kilka warstw?
- Czy `write` to jest finalna operacja, czy dopiero pół drogi?
```

Dobre pytanie rekrutacyjne:

```text
Jak wyglądałby pipeline Bronze -> Silver -> Gold i dlaczego to nie jest tylko 1 DataFrame?
```

<!-- end_slide -->

## 8. STAŁY PATTERN — zapamiętaj to

```text
PYSPARK PIPELINE — stały wzorzec

=== SparkSession ===
spark = SparkSession.builder \
    .appName("OrdersPipeline") \
    .getOrCreate()
# Jeden per job. getOrCreate() bezpieczne do ponownego wywołania.

=== Read ===
df = spark.read.option("inferSchema", "true").json("data/bronze/orders/")
# Bronze = surowe dane na wejściu

=== Transform (Silver) ===
df_silver = df \
    .withColumn("status", F.trim(F.lower(F.col("status")))) \
    .withColumn("total_amount", F.col("total_amount").cast("double")) \
    .filter(F.col("order_id").isNotNull())
# clean + normalize + filter invalid rows

=== Write ===
df_silver.write \
    .mode("overwrite") \
    .partitionBy("status") \
    .parquet("output/silver/orders/")
# action: uruchamia job

CHECKLIST:
[ ] SparkSession.builder.getOrCreate()
[ ] Wszystkie transformacje przed write
[ ] mode("overwrite") dla idempotentności
[ ] partitionBy dla większych tabel
[ ] spark.stop() na końcu lokalnego jobu
```

## 9. Checkpoint: czy rozumiesz to naprawdę?

```text
Jeśli potrafisz odpowiedzieć na te 4 pytania, to jesteś gotowy do labu:
1. Co robi `withColumn`?
2. Co robi `filter` w Spark i kiedy jest uruchomiona?
3. Czym jest `partitionBy` i dlaczego ma sens?
4. Co jest różnicą między `transformation` a `action`?
```

Jeżeli nie potrafisz odpowiedzieć bez patrzenia na kod, wróć do tego pliku i zrób wyjaśnienie na prostym przykładzie `orders` na głos.

<!-- end_slide -->
