# Patterns: Lekcja 05

## Python basics

| Potrzeba | Wzorzec |
|---|---|
| tekst | `status = "completed"` |
| liczba | `amount = 120.50` |
| warunek | `if status == "completed":` |
| lista | `orders = [order1, order2]` |
| rekord | `order = {"status": "completed"}` |
| petla | `for order in orders:` |
| funkcja | `def calculate(...): return result` |
| CSV | `csv.DictReader(file)` |

## Minimalna funkcja

```python
def calculate_completed_revenue(orders: list[dict[str, str]]) -> float:
    revenue = 0.0

    for order in orders:
        if order["status"] == "completed":
            revenue = revenue + float(order["total_amount"])

    return revenue
```

## Review checklist

```text
[ ] Czy funkcja ma jasna nazwe?
[ ] Czy funkcja zwraca wynik przez return?
[ ] Czy kwoty z CSV sa konwertowane przez float?
[ ] Czy petla przechodzi po liscie rekordow?
[ ] Czy test sprawdza konkretny wynik?
```