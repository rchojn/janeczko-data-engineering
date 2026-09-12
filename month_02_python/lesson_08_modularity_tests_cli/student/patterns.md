# Patterns: Lekcja 08

## CLI przez argparse

```python
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
```

## Logging

```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Pipeline started")
```

## Retry z limitem

```python
def retry(operation: Callable[[], T], attempts: int) -> T:
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return operation()
        except OSError as error:
            last_error = error
    raise RuntimeError("Operation failed") from last_error
```

## Testowalna transformacja

```python
def calculate_completed_revenue(records: list[Order]) -> float:
    return sum(order.total_amount for order in records if order.status == "completed")
```
