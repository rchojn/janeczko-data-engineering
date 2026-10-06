"""
dlt_pipeline_local_sim.py — Lokalna symulacja DLT pipeline

UWAGA: To nie jest prawdziwy DLT (wymaga Databricks workspace).
       Symulujemy logikę Bronze → Silver → Gold z lokalnym PySpark + Delta.
       Komentarze pokazują jak to wygląda w prawdziwym DLT.

Uruchomienie:
    python dlt_pipeline_local_sim.py
"""

import shutil

from delta import configure_spark_with_delta_pip
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


# ─────────────────────────────────────────────────────────────────────────────
# Lokalna inicjalizacja — na Databricks: SparkSession jest wstrzyknięty
# ─────────────────────────────────────────────────────────────────────────────

def create_spark() -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("DLTLocalSim")
        .master("local[*]")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.showConsoleProgress", "false")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


# ─────────────────────────────────────────────────────────────────────────────
# WZOR: DLT Bronze layer
#
# W prawdziwym DLT:
# @dlt.table(name="orders_bronze")
# def orders_bronze():
#     return spark.read.json("/Volumes/prod/raw/orders/")
# ─────────────────────────────────────────────────────────────────────────────

def orders_bronze(spark: SparkSession) -> DataFrame:
    """Bronze: raw data ingestion — brak transformacji, brak walidacji."""
    raw = [
        ("1001", "completed", 120.5, "C001"),
        ("1002", "PENDING",    80.0, "C002"),
        ("1003", " Completed ", 240.0, "C001"),
        ("1004", "cancelled",  55.0, "C003"),
        (None,   "completed",  10.0, "C004"),   # zły rekord — null order_id
        ("1005", "completed", -5.0, "C001"),    # zły rekord — ujemna kwota
    ]
    return spark.createDataFrame(raw, ["order_id", "status", "amount", "customer_id"])


# ─────────────────────────────────────────────────────────────────────────────
# WZOR: DLT Silver layer z expectations
#
# W prawdziwym DLT:
# @dlt.expect("valid_order_id", "order_id IS NOT NULL")
# @dlt.expect_or_drop("positive_amount", "amount > 0")
# @dlt.table(name="orders_silver")
# def orders_silver():
#     return dlt.read("orders_bronze").withColumn(...)
# ─────────────────────────────────────────────────────────────────────────────

def orders_silver(df_bronze: DataFrame) -> tuple[DataFrame, int]:
    """Silver: normalizacja + walidacja.

    Lokalna symulacja @dlt.expect_or_drop:
    - null order_id → usunięty
    - ujemna kwota → usunięty
    """
    before_count = df_bronze.count()

    df = (
        df_bronze
        .withColumn("status", F.trim(F.lower(F.col("status"))))
        .filter(F.col("order_id").isNotNull())  # expect: valid_order_id
        .filter(F.col("amount") > 0)            # expect: positive_amount
    )

    dropped = before_count - df.count()
    return df, dropped


# ─────────────────────────────────────────────────────────────────────────────
# WZOR: DLT Gold layer
#
# W prawdziwym DLT:
# @dlt.table(name="revenue_by_customer")
# def revenue_by_customer():
#     return dlt.read("orders_silver").groupBy(...).agg(...)
# ─────────────────────────────────────────────────────────────────────────────

def revenue_by_customer(df_silver: DataFrame) -> DataFrame:
    """Gold: aggregation — revenue per customer dla completed orders."""
    return (
        df_silver
        .filter(F.col("status") == "completed")
        .groupBy("customer_id")
        .agg(F.sum("amount").alias("revenue"))
        .orderBy(F.desc("revenue"))
    )


if __name__ == "__main__":
    shutil.rmtree("output/dlt_sim", ignore_errors=True)

    spark = create_spark()
    spark.sparkContext.setLogLevel("ERROR")

    # Pipeline: Bronze → Silver → Gold
    df_bronze = orders_bronze(spark)
    print(f"[bronze] Rekordów: {df_bronze.count()}")

    df_silver, dropped = orders_silver(df_bronze)
    print(f"[silver] Rekordów: {df_silver.count()} (odrzuconych: {dropped})")

    df_gold = revenue_by_customer(df_silver)
    print("[gold] Revenue by customer:")
    df_gold.show()

    # Zapis jako Delta (lokalnie — na Databricks DLT zarządza tym automatycznie)
    df_silver.write.format("delta").mode("overwrite").save("output/dlt_sim/silver")
    df_gold.write.format("delta").mode("overwrite").save("output/dlt_sim/gold")

    spark.stop()
