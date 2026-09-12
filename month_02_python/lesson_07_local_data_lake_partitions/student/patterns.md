# Patterns: Lekcja 07

## 1. Boundary contract przez Pydantic

```python
from pydantic import BaseModel, Field, field_validator


ALLOWED_STATUSES: set[str] = {"completed", "cancelled", "pending", "refunded"}


class OrderPayload(BaseModel):
    order_id: str = Field(min_length=1)
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            raise ValueError(f"status must be one of: {allowed}")
        return normalized
```

## 2. dataclass jako typ domenowy po walidacji

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"
```

## 3. Rejected record z operacyjnym kontekstem

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RejectedRecord:
    raw_record: dict[str, Any]
    reason: str
    validation_stage: str
    contract_version: str
```

## 4. Routing accepted/rejected

```python
accepted: list[Order] = []
rejected: list[RejectedRecord] = []

for raw_record in raw_records:
    try:
        payload = OrderPayload.model_validate(raw_record)
        accepted.append(
            Order(
                order_id=payload.order_id,
                status=payload.status,
                total_amount=payload.total_amount,
                source=payload.source,
            )
        )
    except Exception as exc:
        rejected.append(
            RejectedRecord(
                raw_record=raw_record,
                reason=str(exc),
                validation_stage="boundary_contract",
                contract_version="v1",
            )
        )
```

## 5. Transform tylko na accepted records

```python
def calculate_completed_revenue(orders: list[Order]) -> float:
    return sum(order.total_amount for order in orders if order.is_completed)
```

## 6. Quality summary pattern

```python
def quality_summary(accepted: list[Order], rejected: list[RejectedRecord]) -> dict[str, object]:
    return {
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "reject_rate": (len(rejected) / (len(accepted) + len(rejected))) if (accepted or rejected) else 0.0,
        "top_reject_reasons": [item.reason for item in rejected[:5]],
        "contract_version": "v1",
    }
```

## 7. Schema drift tests - minimum

```python
def test_missing_order_id_is_rejected() -> None:
    payload = {"status": "completed", "total_amount": "100.00"}
    result = validate_payloads([payload])

    assert result.accepted_count == 0
    assert result.rejected_count == 1
    assert "order_id" in result.rejected_records[0].reason


def test_invalid_status_is_rejected() -> None:
    payload = {"order_id": "1001", "status": "done", "total_amount": "100.00"}
    result = validate_payloads([payload])

    assert result.rejected_count == 1
    assert "status must be one of" in result.rejected_records[0].reason


def test_negative_total_amount_is_rejected() -> None:
    payload = {"order_id": "1001", "status": "completed", "total_amount": -1}
    result = validate_payloads([payload])

    assert result.rejected_count == 1
    assert "greater than or equal to 0" in result.rejected_records[0].reason
```

## 8. Contract evolution pattern

```text
v1 -> baseline fields and enum
v2 -> add optional field (backward compatible)
v3 -> change required field type (breaking)

Rule:
- backward compatible change: accept and log
- breaking change: reject and alert
- every contract change: update model + tests + notes
```

## 9. Multithreading pattern (I/O-bound extract)

```python
from concurrent.futures import ThreadPoolExecutor


def load_many_payloads(paths: list[Path]) -> list[dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=8) as pool:
        chunks = list(pool.map(read_payload_file, paths))
    return [record for chunk in chunks for record in chunk]
```

Use case:

```text
wiele plikow / wolny I/O / brak ciezkich obliczen CPU
```

## 10. Multiprocessing pattern (CPU-bound normalize)

```python
from concurrent.futures import ProcessPoolExecutor


def normalize_many(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    with ProcessPoolExecutor(max_workers=4) as pool:
        return list(pool.map(normalize_record_cpu_heavy, records))
```

Use case:

```text
ciezkie CPU operacje, np. kosztowne regex/hash/parsing
```

## 11. Deterministic merge pattern

```python
def stable_sort_records(records: list[Order]) -> list[Order]:
    return sorted(records, key=lambda item: item.order_id)
```

Po concurrency stabilizuj kolejnosc outputu.
To ogranicza flaky testy snapshotowe.

## 12. Sequential vs parallel parity test

```python
def test_parallel_keeps_same_business_result(sample_records: list[dict[str, Any]]) -> None:
    sequential = validate_payloads(sample_records)
    parallel = validate_payloads_parallel(sample_records, workers=4)

    assert sequential.accepted_count == parallel.accepted_count
    assert sequential.rejected_count == parallel.rejected_count
```

Najpierw rownowaznosc wyniku, dopiero potem pomiar czasu.
