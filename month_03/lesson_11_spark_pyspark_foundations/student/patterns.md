# Patterns: Lekcja 11 — PySpark

## Pattern: Bronze → Silver transform

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("job").master("local[*]").getOrCreate()

df_bronze = spark.read.option("inferSchema", "true").json("data/bronze/")

df_silver = (
    df_bronze
    .withColumn("status", F.trim(F.lower(F.col("status"))))
    .withColumn("amount", F.col("amount").cast("double"))
    .filter(F.col("id").isNotNull())
)

df_silver.write.mode("overwrite").partitionBy("status").parquet("output/silver/")
spark.stop()
```

## Pattern: Testy PySpark

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").appName("test").getOrCreate()

def test_normalize(spark):
    df = spark.createDataFrame([("1", "COMPLETED", 100.0)],
                                ["id", "status", "amount"])
    result = normalize(df)
    assert result.first()["status"] == "completed"
```

## Pattern: Broadcast join (mała tabela)

```python
# dim_table jest mała (< 10 MB) — broadcast unika shuffle
df.join(F.broadcast(dim_table), on="customer_id", how="left")
```

## Pattern: Revenue aggregation

```python
df.filter(F.col("status") == "completed") \
  .groupBy("customer_id") \
  .agg(F.sum("amount").alias("revenue")) \
  .orderBy(F.desc("revenue"))
```

## Anti-patterns

```python
# ŹLE: collect() na dużym DataFrame — wysyła wszystko do drivera
all_rows = df.collect()      # MemoryError przy dużych danych

# DOBRZE: aggregate na executorach, potem show małego wyniku
df.groupBy("status").count().show()

# ŹLE: pętla Python po DataFrame
for row in df.collect(): ...  # to nie jest Spark — to Python na driverze

# DOBRZE: używaj transformacji Spark (withColumn, filter, map przez RDD jeśli musisz)
```
