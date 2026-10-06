# Patterns: Delta Lake

## STAŁY WZORZEC

```python
# DELTA LAKE — stały wzorzec

# === SparkSession z Delta ===
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# === Zapis ===
df.write.format("delta").mode("overwrite").save("path/to/table")

# === Append ===
df.write.format("delta").mode("append").save("path/to/table")

# === Time Travel ===
spark.read.format("delta").option("versionAsOf", 0).load(path)
spark.read.format("delta").option("timestampAsOf", "2026-09-01").load(path)

# === Schema Evolution ===
df.write.format("delta").option("mergeSchema", "true").mode("append").save(path)

# === Historia ===
from delta.tables import DeltaTable
DeltaTable.forPath(spark, path).history().show()
```

## Kiedy co

| Scenariusz | Rozwiązanie |
|-----------|-------------|
| Concurrent writers | Delta (optimistic concurrency) |
| Dodaję kolumnę do tabeli prod | `mergeSchema=true` |
| Bug nadpisał dane — rollback | `versionAsOf` + `mode("overwrite")` |
| Audyt kto co zmienił | `history()` |
| Prosty batch bez update | plain Parquet |
| AWS Athena/Glue | Iceberg |
| Databricks | Delta |
