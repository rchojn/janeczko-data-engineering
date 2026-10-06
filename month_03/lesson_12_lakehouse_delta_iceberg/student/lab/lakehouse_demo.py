"""
lakehouse_demo.py — Demo: Delta Lake lokalnie

Uruchomienie:
    pip install delta-spark==3.2.0 pyspark==3.5.0
    python lakehouse_demo.py

Ta wersja ma format task-driven:
    1. zadanie: zapisz pierwszą wersję tabeli
    2. zadanie: dodaj nową wersję danych
    3. zadanie: sprawdź time travel
    4. zadanie: dodaj nową kolumnę przez schema evolution
    5. zadanie: sprawdź historię commitów
    6. challenge: znajdź błędne założenia i pokaż, co by było w produkcji

To jest zgodne z mocnym podejściem month 01/02: małe kroki, walidacja wyniku, edge case, challenge.
"""

import shutil
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 1: Konfiguracja SparkSession z Delta Lake
# Co robimy:
#   - dodajemy Delta extension do Spark,
#   - to jest warunek, żeby `format("delta")` działało.
# Warto wiedzieć:
#   - Delta to nie zwykły folder z plikami, tylko tabelaryjna warstwa z historią i transakcjami.
# Challenge:
#   - porównaj to z zwykłym Parquetem i zapytaj: co daje nam historia commitów?
# ─────────────────────────────────────────────────────────────────────────────

def create_spark() -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("LakehouseDemo")
        .master("local[*]")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.ui.showConsoleProgress", "false")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 2: Pierwszy zapis do Delta table
# Co robimy:
#   - zapisujemy dane w formacie Delta,
#   - to robi pierwszą wersję tabeli, czyli `version 0`.
# Checkpoint:
#   - czy widzisz różnicę między `delta` a zwykłym `parquet`?
#   - gdzie pojawia się historię odczytu / wersji?
# ─────────────────────────────────────────────────────────────────────────────

def demo_initial_write(spark: SparkSession, path: str) -> None:
    """Wersja 0 — pierwotny zapis."""
    orders = [
        ("1001", "completed", 120.5),
        ("1002", "pending",    80.0),
        ("1003", "completed", 240.0),
        ("1004", "cancelled",  55.0),
    ]
    df = spark.createDataFrame(orders, ["order_id", "status", "amount"])

    df.write.format("delta").mode("overwrite").save(path)
    print(f"[v0] Zapisano {df.count()} rekordów")


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 3: Aktualizacja tabeli z nowymi rekordami
# Co robimy:
#   - dodajemy nową wersję danych przez append,
#   - zmienia się wersja tabeli, a nie tylko plik na dysku,
#   - to modeluje typowy scenariusz: ingestion + incremental update.
# Challenge:
#   - co by się stało, gdybyśmy w tym miejscu zrobili `overwrite` zamiast `append`?
# ─────────────────────────────────────────────────────────────────────────────

def demo_append(spark: SparkSession, path: str) -> None:
    """Wersja 1 — dorzucamy nowe zamówienia."""
    new_orders = [
        ("1005", "completed", 180.0),
        ("1006", "pending",    30.0),
    ]
    df = spark.createDataFrame(new_orders, ["order_id", "status", "amount"])

    df.write.format("delta").mode("append").save(path)
    print(f"[v1] Dorzucono {df.count()} nowych rekordów")


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 4: Time travel
# Co robimy:
#   - czytamy poprzednią wersję tabeli przed append,
#   - to pokazuje, że Delta zachowuje historię danych i umożliwia rollback/porównanie.
# Checkpoint:
#   - ile rekordów miała wersja 0, ile ma obecna tabela?
# ─────────────────────────────────────────────────────────────────────────────

def demo_time_travel(spark: SparkSession, path: str) -> None:
    """Odczytaj poprzednią wersję tabeli."""
    df_v0 = (
        spark.read
        .format("delta")
        .option("versionAsOf", 0)
        .load(path)
    )
    df_current = spark.read.format("delta").load(path)

    print(f"[time travel] v0: {df_v0.count()} rekordów | current: {df_current.count()} rekordów")


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 5: Schema evolution
# Co robimy:
#   - dodajemy kolumnę `region` do istniejącej tabeli,
#   - `mergeSchema=true` pozwala na rozszerzenie schema bez wywołania pełnej rebuild.
# Edge case:
#   - stare rekordy mają `NULL` w nowej kolumnie,
#   - to jest klasyczne zachowanie w schemacie zmieniającym się w czasie.
# ─────────────────────────────────────────────────────────────────────────────

def demo_schema_evolution(spark: SparkSession, path: str) -> None:
    """Dodaj kolumnę 'region' bez przebudowy tabeli."""
    eu_orders = [
        ("1007", "completed", 95.0, "EU"),
        ("1008", "pending",   40.0, "EU"),
    ]
    df = spark.createDataFrame(eu_orders, ["order_id", "status", "amount", "region"])

    (
        df.write
        .format("delta")
        .option("mergeSchema", "true")
        .mode("append")
        .save(path)
    )

    full = spark.read.format("delta").load(path)
    print(f"[schema evolution] Kolumny po dodaniu: {full.columns}")
    print("Rekordy bez region (NULL):")
    full.filter(F.col("region").isNull()).show()


# ─────────────────────────────────────────────────────────────────────────────
# ZADANIE 6: Historia tabeli / commit log
# Co robimy:
#   - sprawdzamy, jakie operacje zostały wykonane na tabeli,
#   - to jest podstawowy element reliability i auditability.
# Challenge:
#   - zastanów się, jak z tej historii odebrałbyś rollback / debug / anomalia danych.
# ─────────────────────────────────────────────────────────────────────────────

def demo_history(spark: SparkSession, path: str) -> None:
    """Pokaż wszystkie operacje na tabeli."""
    dt = DeltaTable.forPath(spark, path)
    print("[history] Historia operacji:")
    dt.history().select("version", "timestamp", "operation").show(truncate=False)


if __name__ == "__main__":
    delta_path = "output/delta/orders"
    shutil.rmtree(delta_path, ignore_errors=True)

    spark = create_spark()
    spark.sparkContext.setLogLevel("ERROR")

    demo_initial_write(spark, delta_path)
    demo_append(spark, delta_path)
    demo_time_travel(spark, delta_path)
    demo_schema_evolution(spark, delta_path)
    demo_history(spark, delta_path)

    spark.stop()
