# Interview Questions: Lekcja 12 — Lakehouse / Delta Lake

## Pytania rekrutacyjne

1. **Czym różni się Delta Lake od plain Parquet?**

   Dobra odpowiedź: Delta dodaje `_delta_log/` — transaction log który sprawia że każda operacja jest atomowa. Plain Parquet to folder z plikami bez żadnej koordynacji. Delta = ACID, time travel, schema enforcement, row-level update. Parquet = szybki read, ale brak transakcji.

2. **Co to jest time travel w Delta Lake i kiedy go używasz?**

   Dobra odpowiedź: Możliwość odczytu poprzedniej wersji tabeli przez `versionAsOf` lub `timestampAsOf`. Używa się do: rollback po błędnym pipeline, audyt zmian danych, debugowanie skąd wzięła się anomalia w raporcie.

3. **Jak Delta Lake obsługuje concurrent writes?**

   Dobra odpowiedź: Optimistic concurrency — każdy writer czyta aktualną wersję, zapisuje, potem waliduje że nikt inny nie pisał w tym samym czasie. Jeśli konflikt → retry. Inaczej niż pesymistyczny lock (jeden writer na raz) — lepsze dla batch ETL.

4. **Czym różni się Delta Lake od Apache Iceberg?**

   Dobra odpowiedź: Oba rozwiązują ten sam problem (ACID na plikach). Delta: rozwinął Databricks, najlepsze wsparcie na Spark/Databricks. Iceberg: zrobił Apple, stał się domyślnym na AWS (Glue, Athena od 2023). W multi-engine środowisku (Trino + Flink + Spark) Iceberg ma lepsze wsparcie. W praktyce: platforma narzuca wybór.

5. **Co to jest schema evolution i czym się różni od schema enforcement?**

   Dobra odpowiedź: Schema enforcement = blokowanie zapisów ze złą schemą (domyślne). Schema evolution = pozwalanie na dodanie nowych kolumn (`mergeSchema=true`). Bez mergeSchema: AnalysisException. Ze starymi rekordami: nowe kolumny = NULL.

6. **Co to jest `_delta_log/` i co w nim jest?**

   Dobra odpowiedź: Folder z plikami JSON — jeden plik per transakcja. Każdy wpis zawiera: listę dodanych plików Parquet, listę usuniętych plików, metadata operacji (timestamp, kto pisał). Delta rekonstruuje stan tabeli czytając log od początku. Co 10 checkpoints log jest kompaktowany do pliku Parquet (dla performance).

---

## Extra: pytania o architekturę

```text
Q: "Jakie masz doświadczenie z Lakehouse?"
A: Powiedz konkretnie:
   - Jakiego formatu używałeś (Delta/Iceberg/plain Parquet)
   - Na jakiej platformie (Databricks / AWS Glue / lokalnie)
   - Jaki problem rozwiązywałeś (concurrent writes / schema drift / rollback)
```

```text
Q: "Kiedy plain Parquet wystarczy?"
Dobra odpowiedź:
- Proste batch ETL bez concurrent writers
- Read-only analytical tables
- Brak potrzeby time travel ani row-level update
- Prototyp / jeden-writer scenario
```

```text
Q: "Co to jest Bronze/Silver/Gold w Lakehouse?"
Bronze: raw dane (landing zone, brak transformacji)
Silver: znormalizowane, filtrowane (JOIN, dedup, schema fix)
Gold: agreagaty gotowe do raportów (metrics, KPIs)
```
