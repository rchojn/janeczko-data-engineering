from __future__ import annotations

import time
from typing import Callable

from pyspark import StorageLevel
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


# spark_internals_demo.py
#
# Cel tego labu:
# 1. Zobaczyc, ze Spark performance to glownie koszt planu wykonania.
# 2. Rozroznic narrow vs wide transformations.
# 3. Porownac shuffle join z broadcast join.
# 4. Wykryc skew i zobaczyc prosty fix przez salting.
# 5. Zobaczyc, kiedy persistence ma sens.
#
# Uruchomienie:
#   python spark_internals_demo.py
#   Spark UI: http://localhost:4040


def create_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName("SparkInternalsDemo")
        .master("local[4]")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.skewJoin.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )


def timed(label: str, action: Callable[[], int]) -> None:
    started_at = time.perf_counter()
    result = action()
    duration = time.perf_counter() - started_at
    print(f"{label:<32} rows={result:<10} time={duration:.2f}s")


def print_header(title: str) -> None:
    print(f"\n{'=' * 18} {title} {'=' * 18}")


def explain_block(title: str, df: DataFrame) -> None:
    print_header(title)
    df.explain(mode="formatted")


def demo_narrow_vs_wide(spark: SparkSession) -> None:
    print_header("NARROW VS WIDE")
    base = spark.range(0, 200_000).withColumn("bucket", (F.col("id") % 10).cast("int"))

    narrow = base.filter(F.col("bucket") < 5).withColumn("double_id", F.col("id") * 2)
    wide = base.groupBy("bucket").count()

    print("Narrow transformation: filter + withColumn")
    print("Wide transformation: groupBy -> shuffle")

    explain_block("PLAN: narrow", narrow)
    explain_block("PLAN: wide", wide)

    timed("narrow.count()", narrow.count)
    timed("wide.count()", wide.count)



def build_orders_and_customers(spark: SparkSession) -> tuple[DataFrame, DataFrame]:
    orders = spark.createDataFrame(
        [(str(i), f"C{i % 500}", float(i % 1000), f"2026-09-{(i % 28) + 1:02d}") for i in range(200_000)],
        ["order_id", "customer_id", "amount", "order_date"],
    )
    customers = spark.createDataFrame(
        [(f"C{i}", f"Customer {i}", "EU" if i % 2 == 0 else "US") for i in range(500)],
        ["customer_id", "customer_name", "region"],
    )
    return orders, customers



def demo_join_strategy(spark: SparkSession) -> None:
    print_header("JOIN STRATEGY")
    orders, customers = build_orders_and_customers(spark)

    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    shuffle_join = orders.join(customers, "customer_id")
    explain_block("PLAN: shuffle join", shuffle_join)

    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(10 * 1024 * 1024))
    broadcast_join = orders.join(F.broadcast(customers), "customer_id")
    explain_block("PLAN: broadcast join", broadcast_join)

    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    timed("shuffle join count()", shuffle_join.count)

    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(10 * 1024 * 1024))
    timed("broadcast join count()", broadcast_join.count)

    print("\nCheck:")
    print("- Exchange / SortMergeJoin = shuffle i drozszy join")
    print("- BroadcastHashJoin = mala tabela wyslana do executorow")



def build_skewed_facts(spark: SparkSession) -> tuple[DataFrame, DataFrame]:
    orders = spark.createDataFrame(
        [("US", f"O{i}", float(i % 100)) for i in range(180_000)]
        + [("PL", f"O{i}", float(i % 100)) for i in range(10_000)]
        + [("DE", f"O{i}", float(i % 100)) for i in range(10_000)],
        ["country", "order_id", "amount"],
    )
    country_dim = spark.createDataFrame(
        [("US", "North America"), ("PL", "Europe"), ("DE", "Europe")],
        ["country", "region"],
    )
    return orders, country_dim



def demo_skew_detection_and_fix(spark: SparkSession) -> None:
    print_header("SKEW")
    orders, country_dim = build_skewed_facts(spark)

    print("Rozklad danych po kluczu:")
    orders.groupBy("country").count().orderBy(F.desc("count")).show()

    skewed_join = orders.join(country_dim, "country")
    explain_block("PLAN: skewed join", skewed_join)
    timed("skewed join count()", skewed_join.count)

    salt_factor = 8
    salted_orders = orders.withColumn("salt", (F.rand(seed=42) * salt_factor).cast("int"))
    salted_dim = country_dim.crossJoin(
        spark.range(0, salt_factor).withColumnRenamed("id", "salt")
    )

    salted_join = salted_orders.join(salted_dim, ["country", "salt"])
    explain_block("PLAN: salted join", salted_join)
    timed("salted join count()", salted_join.count)

    print("\nCheck:")
    print("- skew = jeden klucz dominuje i blokuje caly stage")
    print("- salting rozklada najciezszy klucz na kilka wariantow")
    print("- w realnej pracy najpierw sprawdzasz AQE, potem dopiero reczne salting")



def demo_persistence(spark: SparkSession) -> None:
    print_header("PERSISTENCE")
    orders, customers = build_orders_and_customers(spark)
    joined = orders.join(F.broadcast(customers), "customer_id")

    print("Ta sama tabela jest liczona dwa razy: raz revenue, raz orders_count.")

    timed(
        "without cache revenue",
        lambda: int(joined.groupBy("region").agg(F.sum("amount")).count()),
    )
    timed(
        "without cache orders",
        lambda: int(joined.groupBy("region").agg(F.count("order_id")).count()),
    )

    cached = joined.persist(StorageLevel.MEMORY_AND_DISK)
    cached.count()

    timed(
        "with cache revenue",
        lambda: int(cached.groupBy("region").agg(F.sum("amount")).count()),
    )
    timed(
        "with cache orders",
        lambda: int(cached.groupBy("region").agg(F.count("order_id")).count()),
    )

    cached.unpersist()
    print("\nCheck:")
    print("- cache ma sens, gdy ten sam DataFrame jest uzywany wiele razy")
    print("- cache nie jest darmowy: zuzywa memory i moze prowokowac spills")



def main() -> None:
    spark = create_spark()
    spark.sparkContext.setLogLevel("ERROR")

    print("Spark UI: http://localhost:4040")
    print("Przy kazdym demie odpowiedz: gdzie jest shuffle, gdzie jest skew, jaki jest fix.")

    demo_narrow_vs_wide(spark)
    demo_join_strategy(spark)
    demo_skew_detection_and_fix(spark)
    demo_persistence(spark)

    print_header("CLOSING CHECK")
    print("1. Czy umiesz wskazac Exchange w explain()?")
    print("2. Czy umiesz powiedziec, kiedy broadcast join ma sens?")
    print("3. Czy umiesz odroznic skew od samego duzego wolumenu danych?")
    print("4. Czy umiesz powiedziec, kiedy cache pomaga, a kiedy przeszkadza?")

    spark.stop()


if __name__ == "__main__":
    main()
