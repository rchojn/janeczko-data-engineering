# Patterns: Spark Internals

```python
# SPARK INTERNALS — staly wzorzec

# === 1. Pierwszy check planu ===
df.explain(mode="formatted")
# Exchange = shuffle
# BroadcastHashJoin = broadcast
# SortMergeJoin = obie strony ida przez drozszy join

# === 2. Wykryj skew po kluczu ===
df.groupBy("key_col").count().orderBy(F.desc("count")).show(10)
# top 1 >> reszta = candidate do skew

# === 3. Broadcast join dla malej tabeli ===
result = df_large.join(F.broadcast(df_small), "key")
# mniej shuffle, jesli df_small jest rzeczywiscie mala

# === 4. AQE zostaw wlaczone ===
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# === 5. Partycje ===
df.rdd.getNumPartitions()
df.repartition(16)   # rowny rozklad, ale z shuffle
df.coalesce(4)       # mniej partycji bez shuffle

# === 6. Cache tylko przy ponownym uzyciu ===
cached = df.persist(StorageLevel.MEMORY_AND_DISK)
cached.count()   # materializacja
# ... uzycie kilka razy ...
cached.unpersist()

# === 7. Skew fix przez salting ===
salt_factor = 8
left = left.withColumn("salt", (F.rand(seed=42) * salt_factor).cast("int"))
right = right.crossJoin(spark.range(0, salt_factor).withColumnRenamed("id", "salt"))
result = left.join(right, ["key", "salt"])
```

## Kiedy co

| Problem | Pierwszy check | Typowy fix |
|---------|----------------|------------|
| Wolny join | `explain()` | broadcast albo lepszy key |
| Jeden task trwa 10x dluzej | `groupBy(key).count()` i Spark UI | AQE albo salting |
| Za duzo malych taskow | `df.rdd.getNumPartitions()` | mniej partycji / coalesce |
| Za malo rownoleglosci | stage ma malo taskow | repartition |
| Ten sam DF liczony kilka razy | powtorne akcje | cache/persist |
| Wolny write i masa plikow | output file layout | coalesce przed write albo lepszy partitioning |

## Staly review recipe

```text
1. Explain
2. Exchange?
3. Join strategy?
4. Skew?
5. AQE?
6. Partitions?
7. Cache?
8. Write layout?
```
