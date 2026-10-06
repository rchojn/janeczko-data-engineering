# Interview questions: Lekcja 11 — PySpark

1. Kiedy wybrałbyś PySpark zamiast Polars?
2. Co to lazy evaluation w Sparku?
3. Czym różni się transformation od action? Podaj przykłady.
4. Po co partycjonować dane przy zapisie?
5. Co to shuffle i dlaczego jest kosztowny?
6. Dlaczego zapisujesz Parquet zamiast CSV?

Dobra odpowiedź: problem → narzędzie → konsekwencja w pipeline.

---

## Pytania — Spark internals (często na rekrutacji)

7. Co to DAG w Sparku?

   DAG (Directed Acyclic Graph) = graf zależności między transformacjami.
   Spark buduje DAG na podstawie Twojego kodu, optymalizuje go (Catalyst), potem wykonuje.
   Możesz zobaczyć DAG w Spark UI pod `localhost:4040` podczas joba.

8. Co to shuffle i jak go minimalizować?

```text
Shuffle = transfer danych między executorami przez sieć.
Drogi: join dwóch dużych tabel, groupBy z dużą kardynalnością.

Jak minimalizować:
- broadcast join gdy jedna tabela jest mała (< 10 MB)
  df.join(F.broadcast(dim_df), "id")
- partitionBy przed joinami (pre-partition)
- filtruj jak najwcześniej (partition pruning)
```

9. Co to skew i jak go naprawić?

   Skew = jedna partycja ma dużo więcej danych niż inne → jeden executor blokuje cały job.
   Przyczyna: join na kluczu który ma nierówny rozkład (np. "unknown" = 80% rekordów).
   Fix: salt key albo skew hint w Sparku 3.x.

10. Jak testujesz PySpark lokalnie bez klastra?

```python
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local[2]") \
        .appName("test") \
        .getOrCreate()

def test_normalize_status(spark):
    df = spark.createDataFrame([("1001", "COMPLETED", 100.0)],
                                ["order_id", "status", "total_amount"])
    result = normalize(df)
    assert result.collect()[0]["status"] == "completed"
```

`scope="session"` — jedna sesja Spark dla wszystkich testów (szybciej).

11. Co robi `repartition` a co `coalesce`?

```text
repartition(N):  shuffle — równomierny podział na N partycji
                 użyj gdy chcesz zwiększyć lub równomiernie rozłożyć

coalesce(N):     bez shuffle — łączy istniejące partycje
                 użyj gdy chcesz zmniejszyć (np. przed zapisem do 1 pliku)
```
