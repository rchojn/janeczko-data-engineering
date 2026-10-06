# Patterns: Databricks Platform

```python
# DATABRICKS PLATFORM — stały wzorzec

# === Unity Catalog namespace ===
# catalog.schema.table
# prod.finance.orders
# dev.ml.features_v2

# === OPTIMIZE (small files fix) ===
from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, path)
dt.optimize().executeCompaction()

# === ZORDER (column sorting dla pruning) — Databricks only ===
dt.optimize().executeZOrderBy("customer_id", "order_date")

# === VACUUM ===
dt.vacuum(retentionHours=168)   # 7 dni — NIGDY krócej w produkcji

# === Historia ===
dt.history().select("version", "timestamp", "operation").show()

# === Sprawdź liczbę plików (lokalnie) ===
from pathlib import Path
files = list(Path(path).rglob("*.parquet"))
print(f"Pliki Parquet: {len(files)}")
```

## Kiedy co

| Operacja | Kiedy |
|----------|-------|
| OPTIMIZE | Po serii appendów (daily cron albo ad-hoc po bulk load) |
| VACUUM | Co tydzień, retention min 168h |
| ZORDER | Kolumny używane w WHERE / JOIN często |
| column masking | PII data, GDPR, różne role widzą różne dane |
