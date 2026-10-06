"""
delta_production_ops.py — Demo: OPTIMIZE, VACUUM, small files problem

Uruchomienie:
    python delta_production_ops.py

Czego się uczysz:
    1. Small files problem: wiele appendów = wiele małych plików
    2. OPTIMIZE: kompaktacja do dużych plików
    3. VACUUM: usunięcie starych plików (po retention window)
    4. history(): audit zmian
"""

import shutil
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


DELTA_PATH = "output/delta/prod_orders"


def create_spark() -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("DeltaProductionOps")
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


def count_parquet_files(path: str) -> int:
    """Policz pliki Parquet w folderze (nie w _delta_log/)."""
    return len([p for p in Path(path).rglob("*.parquet")])


def simulate_many_appends(spark: SparkSession, path: str, num_batches: int = 10) -> None:
    """Symuluj wiele małych appendów — realistyczny batch pipeline."""
    for i in range(num_batches):
        batch = spark.createDataFrame(
            [(str(i * 100 + j), "completed", float(j * 10)) for j in range(100)],
            ["order_id", "status", "amount"],
        )
        batch.write.format("delta").mode("append").save(path)

    file_count = count_parquet_files(path)
    print(f"[small files] Po {num_batches} appendach: {file_count} plików Parquet")
    print("  → każdy append tworzy nowy plik = small files problem")


def run_optimize(path: str) -> None:
    """OPTIMIZE: kompaktacja małych plików w większe.

    Na lokalnym Spark: ograniczone możliwości ZORDER (brak DataSkipping index).
    Na Databricks: ZORDER tworzy indeks do partition pruning.
    """
    dt = DeltaTable.forPath(spark, path)
    dt.optimize().executeCompaction()

    file_count = count_parquet_files(path)
    print(f"[optimize] Po OPTIMIZE: {file_count} pliku/plików Parquet")
    print("  → małe pliki połączone w większe = szybszy read")


def run_vacuum(path: str, retention_hours: int = 0) -> None:
    """VACUUM: usuń pliki starsze niż retention threshold.

    UWAGA: retention_hours=0 tylko do demonstracji.
    W produkcji: minimum 168h (7 dni) — inaczej tracisz time travel.
    """
    # Wyłącz safety check dla demo (w produkcji NIE rób tego)
    spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false")

    dt = DeltaTable.forPath(spark, path)
    dt.vacuum(retentionHours=retention_hours)

    file_count = count_parquet_files(path)
    print(f"[vacuum] Po VACUUM(retentionHours={retention_hours}): {file_count} pliku/plików")
    print("  → stare pliki usunięte, time travel do starszych wersji niemożliwy")


def show_history(path: str) -> None:
    """Pokaż całą historię operacji na tabeli."""
    dt = DeltaTable.forPath(spark, path)
    print("\n[history] Historia operacji:")
    dt.history().select("version", "timestamp", "operation", "operationMetrics").show(
        truncate=False
    )


if __name__ == "__main__":
    shutil.rmtree(DELTA_PATH, ignore_errors=True)

    spark = create_spark()
    spark.sparkContext.setLogLevel("ERROR")

    simulate_many_appends(spark, DELTA_PATH, num_batches=10)
    run_optimize(DELTA_PATH)
    run_vacuum(DELTA_PATH, retention_hours=0)
    show_history(DELTA_PATH)

    spark.stop()
