from __future__ import annotations

# spark_databricks_local_sim.py
#
# Ten plik nie udaje prawdziwego workspace Databricks.
# Ma tylko pomoc zmapowac lokalny Spark ETL na kroki,
# ktore w Databricks widzisz jako: compute -> notebook -> Delta -> job.

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def create_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName("SparkDatabricksLocalSim")
        .master("local[*]")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )


def main() -> None:
    spark = create_spark()
    spark.sparkContext.setLogLevel("ERROR")

    print("STEP 1: compute")
    print("Lokalnie compute = SparkSession local[*]")
    print("W Databricks compute = cluster, job compute albo serverless")

    print("\nSTEP 2: notebook logic")
    df = spark.createDataFrame(
        [(1, "created", 120.0), (2, "paid", 300.0), (3, "paid", 50.0)],
        ["order_id", "status", "amount"],
    )

    result = (
        df.filter(F.col("status") == "paid")
        .groupBy("status")
        .agg(F.sum("amount").alias("paid_revenue"))
    )
    result.show()

    print("\nSTEP 3: output")
    print("Tutaj lokalnie tylko pokazujemy wynik DataFrame.")
    print("W Databricks celem bylaby Delta table, nie tylko display().")

    print("\nSTEP 4: checkpoint / incremental")
    print("Lokalna symulacja nie robi Auto Loader.")
    print("W Databricks przy incremental ingest musisz nazwac checkpoint location.")

    print("\nSTEP 5: job")
    print("Lokalnie odpalasz python script recznie.")
    print("W Databricks ten sam flow opakowujesz jako scheduled job.")

    spark.stop()


if __name__ == "__main__":
    main()
