"""
spark_basics.py — Lekcja 11: PySpark w akcji

Uruchomienie:
    python spark_basics.py

Wymagania:
    pip install pyspark==3.5.0
    java -version  ← musi działać (Java 11 lub 17)

Ta wersja labu ma format task-driven:
    1. zadanie: przygotuj dane testowe
    2. zadanie: utwórz SparkSession
    3. zadanie: przeczytaj Bronze
    4. zadanie: zrób transform do Silver
    5. zadanie: policz revenue per customer
    6. zadanie: zapisz output
    7. challenge: dodaj edge case i popraw logiczne błędy

To jest zgodne z podejsciem month 02: mały krok -> sprawdzenie -> edge case -> challenge.
"""

import json
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 1: Przygotowanie danych testowych
# Co robimy:
#   - tworzymy lokalne pliki JSON, które będą wyglądały jak raw bronze data,
#   - to symuluje dane pochodzące z API / CSV / event stream,
#   - w praktyce to jest punkt wejścia do pipeline'u.
# Co sprawdzamy:
#   - czy mamy `null`, duże litery, białe znaki i różne statusy,
#   - to jest bardzo typowe dla surowych danych z produkcji.
# Challenge:
#   - dodaj jeszcze jeden rekord z `status` = "" lub `total_amount` = "abc",
#   - zobacz, co będzie po transformacji.
# ─────────────────────────────────────────────────────────────────────────────
ORDERS = [
    {"order_id": "1001", "status": "completed",   "total_amount": 120.5,  "customer_id": "C001"},
    {"order_id": "1002", "status": "pending",      "total_amount": 80.0,   "customer_id": "C002"},
    {"order_id": "1003", "status": "Completed",    "total_amount": 240.0,  "customer_id": "C001"},
    {"order_id": "1004", "status": " CANCELLED ",  "total_amount": 55.0,   "customer_id": "C003"},
    {"order_id": "1005", "status": "completed",    "total_amount": 99.0,   "customer_id": "C002"},
    {"order_id": None,   "status": "completed",    "total_amount": 10.0,   "customer_id": "C004"},
]

bronze_dir = Path("data/bronze/orders")
bronze_dir.mkdir(parents=True, exist_ok=True)
for i, order in enumerate(ORDERS):
    (bronze_dir / f"order_{i}.json").write_text(json.dumps(order))


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 2: SparkSession
# Co robimy:
#   - tworzymy jednej sesji Spark na cały job,
#   - to jest standard dla każdej lokalnej aplikacji PySpark.
# Warto pamiętać:
#   - `master("local[*]")` = uruchom lokalnie na wszystkich rdzeniach,
#   - `getOrCreate()` = nie tworzy nowych sesji przy kolejnych uruchomieniach.
# ─────────────────────────────────────────────────────────────────────────────
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("OrdersPipeline")
    .master("local[*]")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 3: Odczyt raw Bronze
# Co robimy:
#   - czytamy surowe dane JSON jako DataFrame,
#   - sprawdzamy schemat i rekordy, żeby zobaczyć jak wygląda dane wejściowe.
# Dobre praktyki:
#   - `inferSchema=True` jest OK do demo,
#   - w produkcji zwykle sie definiuje schema jawnie.
# Checkpoint:
#   - czy widzisz rząd z `None` / casing / whitespace?
# ─────────────────────────────────────────────────────────────────────────────

df_bronze = spark.read.option("inferSchema", "true").json(str(bronze_dir))

print("=== Bronze schema ===")
df_bronze.printSchema()

print("=== Bronze records ===")
df_bronze.show(truncate=False)
print(f"Partycje: {df_bronze.rdd.getNumPartitions()}")


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 4: Transformacja Bronze -> Silver
# Co robimy:
#   - normalizujemy status do lowercase,
#   - usuwamy białe znaki,
#   - zamieniamy typ `total_amount` na double,
#   - usuwamy rekordy bez `order_id`.
# To jest typowy pattern w ETL:
#   - clean + normalize + filter invalid rows.
# Challenge:
#   - dodaj walidację: nie pozwól `total_amount` < 0,
#   - spróbuj dodać `status in ("completed", "pending", "cancelled")`.
# ─────────────────────────────────────────────────────────────────────────────

df_silver = (
    df_bronze
    .withColumn("status", F.trim(F.lower(F.col("status"))))
    .withColumn("total_amount", F.col("total_amount").cast("double"))
    .filter(F.col("order_id").isNotNull())
)

print("=== Silver schema ===")
df_silver.printSchema()

print("=== Silver records (po transformacji) ===")
df_silver.show(truncate=False)


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 5: Revenue per customer
# Co robimy:
#   - filtrujemy tylko completed orders,
#   - grupujemy po `customer_id`,
#   - sumujemy przychód.
# To jest bardzo praktyczny raport biznesowy z danych sprzedażowych.
# Checkpoint:
#   - czy wynik ma sens i czy suma nie zawiera zbyt wielu błędnych rekordów?
# ─────────────────────────────────────────────────────────────────────────────

df_revenue = (
    df_silver
    .filter(F.col("status") == "completed")
    .groupBy("customer_id")
    .agg(F.sum("total_amount").alias("revenue"))
    .orderBy(F.desc("revenue"))
)

print("=== Revenue per customer ===")
df_revenue.show()


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 6: Zapis Silver do Parquet
# Co robimy:
#   - zapisujemy sfinalizowaną warstwę danych do folderu output,
#   - `partitionBy("status")` pozwala na mniejsze odczyty i lepsze pruning.
# Dobre praktyki:
#   - `mode("overwrite")` jest bezpieczny dla rerunów lokalnych,
#   - w produkcji dodajesz kontrolę walidacji i metadane pipeline'u.
# ─────────────────────────────────────────────────────────────────────────────

silver_path = "output/silver/orders"

df_silver.write \
    .mode("overwrite") \
    .partitionBy("status") \
    .parquet(silver_path)

print(f"=== Zapisano Silver do {silver_path} ===")

for root, dirs, files in os.walk(silver_path):
    for f in files:
        print(os.path.join(root, f))


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 7: Walidacja roundtrip
# Co robimy:
#   - odczytujemy zapisany output z powrotem,
#   - upewniamy się, że job jest idempotentny i dane zostały zapisane poprawnie.
# Challenge:
#   - dodaj `count()` porównujące liczbę wyjściową z wejściową po filtrach,
#   - pokaż, co dzieje się, gdy usuniesz `null` / zły status.
# ─────────────────────────────────────────────────────────────────────────────

df_verify = spark.read.parquet(silver_path)
print(f"\n=== Weryfikacja: wczytano {df_verify.count()} rekordów z Parquet ===")
df_verify.show()

# Jakie są kolejne kroki w produkcji?
# 1. dodać checki jakości danych,
# 2. dodać monitorowanie zależności,
# 3. dodać czytelny kontrakt schema,
# 4. dodać lokalny/CI test dla transformacji.

spark.stop()
print("Done.")
