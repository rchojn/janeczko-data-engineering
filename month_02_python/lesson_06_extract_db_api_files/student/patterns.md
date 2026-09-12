# Patterns: Lekcja 06

## 1. Extract bez transformacji

```python
def read_orders_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as file:
        return list(csv.DictReader(file))
```

## 2. Required fields check

```python
def validate_required_fields(record: dict[str, str], required_fields: set[str]) -> bool:
    return all(record.get(field) for field in required_fields)
```

## 3. Pydantic jako bramka walidacyjna

```python
class OrderPayload(BaseModel):
    order_id: str
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"
```

## 4. dataclass jako rekord domenowy

```python
@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str
```

## 5. Transform jako czysta funkcja

```python
def calculate_completed_revenue(records: list[Order]) -> float:
    return sum(order.total_amount for order in records if order.is_completed)
```

## 6. Rejected records z powodem

```python
@dataclass(frozen=True)
class RejectedRecord:
    record: dict[str, object]
    reason: str
```

## 7. Load jako osobny krok

```python
def write_json_output(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
```
