# Teoria: Lekcja 09 — ściąga do pracy domowej

Ten plik to ściąga do użycia PODCZAS pracy domowej.
Teoria jest na slajdach — tu masz kod referencyjny, tabele i checklistę.

## PySpark vs Polars

Zanim zaczniesz uczyć się PySpark, wiedz co już znasz.

```python
# Polars (lokalne)
df.filter(pl.col("status") == "completed")
df.with_columns(pl.col("amount").cast(pl.Float64))
df.group_by("status").agg(pl.sum("amount"))

# PySpark (klaster)
df.filter(df.status == "completed")
df.withColumn("amount", df.amount.cast("double"))
df.groupBy("status").agg({"amount": "sum"})
```

Różnice:
- PySpark: lazy evaluation, działa na klastrze, `withColumn` nie `with_columns`
- Polars: eager/lazy, działa lokalnie lub na jednej maszynie, szybszy na małych danych

**Kiedy PySpark:** dane > kilkaset GB, klaster Spark dostępny (EMR, Databricks, GKE).
**Kiedy Polars:** pipeline lokalny lub single-node, szybki prototyp, < 100 GB.

## Boto3 — klient S3

```python
import boto3
from pathlib import Path

# Klient — jeden per sesja, nie per operacja
s3 = boto3.client("s3", region_name="eu-west-1")

# Upload
s3.upload_file("output/orders.parquet", "my-bucket", "orders/orders.parquet")

# Download
s3.download_file("my-bucket", "orders/orders.parquet", "/tmp/orders.parquet")

# List objects
response = s3.list_objects_v2(Bucket="my-bucket", Prefix="orders/")
keys = [obj["Key"] for obj in response.get("Contents", [])]
```

Wzorzec błędów:

```python
from botocore.exceptions import ClientError

try:
    s3.download_file(bucket, key, local_path)
except ClientError as exc:
    if exc.response["Error"]["Code"] == "NoSuchKey":
        raise FileNotFoundError(f"S3 key not found: {key}") from exc
    raise
```

## Avro — format streamingowy

**Parquet vs Avro:**

| Kryterium | Parquet | Avro |
|-----------|---------|------|
| Layout | columnar | row-based |
| Kompresja | świetna przy query | dobra przy write |
| Zastosowanie | batch analytics | Kafka messages, API events |
| Schema | per file (embedded) | per file (embedded) |
| Python library | `polars`, `pyarrow` | `fastavro` |

```python
import fastavro
from io import BytesIO

SCHEMA = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "total_amount", "type": "double"},
    ],
}

# Zapis
records = [
    {"order_id": "1001", "status": "completed", "total_amount": 120.5},
]
buf = BytesIO()
fastavro.writer(buf, fastavro.parse_schema(SCHEMA), records)

# Odczyt
buf.seek(0)
loaded = list(fastavro.reader(buf))
```

## HTTP API z retry i paginacją

```python
import httpx
from typing import Any

def fetch_all_orders(base_url: str, api_key: str) -> list[dict[str, Any]]:
    """Pobiera wszystkie strony wyników z API."""
    all_records: list[dict[str, Any]] = []
    next_cursor: str | None = None

    with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, timeout=10) as client:
        while True:
            params = {"cursor": next_cursor} if next_cursor else {}
            response = client.get(f"{base_url}/orders", params=params)
            response.raise_for_status()
            data = response.json()
            all_records.extend(data["results"])
            next_cursor = data.get("next")  # None gdy ostatnia strona
            if not next_cursor:
                break

    return all_records
```

Wersja produkcyjna powinna rozdzielac:

```text
logika paginacji
logika retry
klasyfikacja bledow retryable / non-retryable
```

Przyklad helpera retry z exponential backoff i jitter:

```python
import random
import time

RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


def retryable_get(
    client: httpx.Client,
    url: str,
    params: dict[str, Any],
    max_attempts: int = 4,
    base_delay: float = 0.5,
) -> httpx.Response:
    for attempt in range(max_attempts):
        response = client.get(url, params=params)

        if response.status_code in RETRYABLE_STATUS_CODES and attempt < max_attempts - 1:
            jitter = random.uniform(0.0, 0.2)
            delay = base_delay * (2 ** attempt) + jitter
            time.sleep(delay)
            continue

        response.raise_for_status()
        return response

    raise RuntimeError("unreachable")
```

Zasady praktyczne:

```text
retry tylko dla bledow przejsciowych (timeout, rate-limit, 5xx),
zawsze ustaw limit prob (brak infinite retry),
dla POST wymagaj idempotency key, inaczej ryzyko duplikatow,
loguj numer proby, status code i finalny outcome.
```

W tej lekcji retry dotyczy integracji IO (API/S3).
W lekcji 07 kontrakty danych dalej nie sa retryowane na validation errors.

## STALY PATTERN — zapamietaj to

```text
EKOSYSTEM DE — staly pattern

=== Boto3 klient ===
s3 = boto3.client("s3", region_name="eu-west-1")
s3.upload_file(local_path, bucket, key)
# Klient raz per sesja. Error = ClientError z kodem.

=== Avro write/read ===
schema = fastavro.parse_schema(SCHEMA_DICT)
fastavro.writer(buf, schema, records)
loaded = list(fastavro.reader(buf))
# Schema embedded. Użyj przy Kafka, streaming events.

=== HTTP API pagination ===
next_cursor = data.get("next")
if not next_cursor:
    break
# Pętla while + cursor = standard dla REST API.

=== Retry z backoff ===
if status in {429, 500, 502, 503, 504}:
    sleep(base * 2**attempt + jitter)
# Retry tylko dla transient errors, z limitem prob.

=== PySpark vs Polars ===
# Polars: pl.col("x").cast(pl.Float64)
# PySpark: df.withColumn("x", df.x.cast("double"))
# Ten sam model — inne nazwy metod.

CHECKLIST:
[ ] Boto3 client tworzony raz, nie per operacja
[ ] ClientError obsłużony z kodem błędu
[ ] Avro schema zdefiniowana jako dict przed zapisem
[ ] HTTP: raise_for_status() przed json()
[ ] Retry ma exponential backoff i limit prob
[ ] Retry dotyczy tylko transient errors
[ ] Paginacja: while True + break na None cursor
[ ] Zewnętrzne systemy mockowane w testach
```
