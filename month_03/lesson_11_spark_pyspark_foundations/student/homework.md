# Praca domowa: Lekcja 11

## Cel

Masz pokazać, że rozumiesz, kiedy Spark ma sens i jak wygląda poprawny pipeline Bronze → Silver w praktyce.

To nie jest tylko "napisać skrypt", tylko odpowiedzieć na pytania:

```text
Co jest raw?
Co jest clean?
Co musi zostać znormalizowane?
Jak sprawdzisz, że wynik jest spójny?
```

<!-- end_slide -->

## Co i gdzie oddajesz

Twój finalny katalog powinien wyglądać mniej więcej tak:

```text
homework/lesson_11/
├── spark_bronze_to_silver.py
├── tests/
│   └── test_transform.py
├── data/
│   └── bronze/
│       └── orders.json
├── output/
│   └── silver/
└── README.md
```

`student/lab/` jest dla nauki i eksperymentów. `homework/lesson_11/` to finalny artefakt do review.

<!-- end_slide -->

## Dane wejściowe

Utwórz lokalny plik z danymi raw:

```json
[
  {"order_id": "1001", "status": "completed",  "total_amount": 120.5,  "customer_id": "C001"},
  {"order_id": "1002", "status": "PENDING",    "total_amount": 80.0,   "customer_id": "C002"},
  {"order_id": "1003", "status": " Completed", "total_amount": 240.0,  "customer_id": "C001"},
  {"order_id": "1004", "status": "cancelled",  "total_amount": 55.0,   "customer_id": "C003"},
  {"order_id": null,   "status": "completed",  "total_amount": 10.0,   "customer_id": "C004"}
]
```

To jest minimalny "bronze dataset". Widzisz od razu 3 problemy:

- status ma różny format,
- `total_amount` może być stringiem,
- `order_id` może być null.

<!-- end_slide -->

## Krok 1: SparkSession

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("OrdersBronzeToSilver")
    .master("local[*]")
    .getOrCreate()
)
```

Zasada: jedna sesja Spark na job, nie ręczne tworzenie głębokich struktur w pętli.

<!-- end_slide -->

## Krok 2: Czytaj dane raw

```python
df_bronze = spark.read.option("inferSchema", "true").json("data/bronze/orders.json")
```

Sprawdź schema i kilka rekordów. To nie jest zbędne — to pierwszy warunek kontroli jakości wejścia.

<!-- end_slide -->

## Krok 3: Transformacja do Silver

Znormalizuj dane według reguł biznesowych:

- `status` -> lowercase + strip
- `total_amount` -> double
- `order_id` -> usuń null / nieprawidłowe rekordy
- zostaw tylko kolumny potrzebne do dalszej analityki

W praktyce `Silver` jest "clean layer". Nie zmieniasz danych w sposób losowy. Zmieniasz format i semantykę tak, aby były spójne.

```python
from pyspark.sql import functions as F

df_silver = (
    df_bronze
    .withColumn("status", F.trim(F.lower(F.col("status"))))
    .withColumn("total_amount", F.col("total_amount").cast("double"))
    .filter(F.col("order_id").isNotNull())
)
```

<!-- end_slide -->

## Krok 4: Zapis do Silver

```python
df_silver.write \
    .mode("overwrite") \
    .partitionBy("status") \
    .parquet("output/silver/orders")
```

Uwaga: `overwrite` jest poprawny, jeśli chcesz zrobic pipeline idempotentny i powtarzalny przy lokalnym testowaniu. To nie jest "czyścimy wszystko bez myślenia", tylko kontrolujemy stan outputu.

<!-- end_slide -->

## Krok 5: Testy jednostkowe

Minimum 3 testy:

1. status po normalizacji jest lowercase,
2. rekordy z null `order_id` nie trafiają do Silver,
3. suma `total_amount` dla completed jest zgodna z oczekiwaniem.

Przykład testu:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[2]").appName("test").getOrCreate()

def test_status_normalized(spark):
    df = spark.createDataFrame([("1001", " COMPLETED ", 120.5)], ["order_id", "status", "total_amount"])
    result = normalize(df)
    assert result.collect()[0]["status"] == "completed"
```

Nie testuj tylko "czy skrypt działa". Testuj reguły biznesowe danych.

<!-- end_slide -->

## Krok 6: Odpowiedzi kontrolne

Zanim oddasz pracę, odpowiedz sobie na 4 pytania:

```text
1. Czego nie robi Bronze?
2. Czego nie robi Silver?
3. Czy pipeline jest idempotentny?
4. Co by się stało, gdyby status nie był znormalizowany?
```

To jest ważna część pracy: nie tylko kod, ale rozumienie semantyki warstw.

<!-- end_slide -->

## Acceptance criteria

- [ ] `python spark_bronze_to_silver.py` uruchamia się bez błędów
- [ ] `output/silver/orders` zawiera partycje po `status`
- [ ] rekordy z `order_id = null` są odfiltrowane
- [ ] `status` jest znormalizowany do lowercase + trim
- [ ] `total_amount` jest poprawnie castowany do `double`
- [ ] `pytest tests/` przechodzi dla minimum 3 testów

<!-- end_slide -->
