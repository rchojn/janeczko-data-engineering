---
title: Lekcja 06 - Python w Data Engineeringu
author: Data Engineering Course
date: 2026-08-14
---

# Lekcja 06

Python w Data Engineeringu

```text
extract -> Pydantic validation -> dataclass records -> transform -> load
```

Dzis przechodzimy od skladni Pythona do malego pipeline'u.

<!-- end_slide -->

# Po co ta lekcja

Na rozmowie nie pytaja tylko o petle.

Czesto pytaja:

```text
Jak pobierasz dane?
Jak sprawdzasz, czy payload ma sens?
Jak dzielisz kod na kroki?
Jak testujesz bez prawdziwego API?
Co zrobisz, gdy rekord jest bledny?
```

<!-- end_slide -->

# Mental model

```text
extract
  pobierz dane z pliku/API/DB

validate
  Pydantic sprawdza pola, typy, status i kwote

domain record
  dataclass Order reprezentuje poprawny rekord

transform
  zamien typy i policz wynik

load
  zapisz output
```

Kazdy krok ma inna odpowiedzialnosc.

<!-- end_slide -->

# Przyklad z lekcji

Dwa wejscia:

```text
orders.csv
api_orders.json
```

Jeden output:

```text
output/pipeline_output.json
```

Nie potrzebujemy prawdziwego API, zeby nauczyc sie struktury pipeline'u.

<!-- end_slide -->

# Extract

```python
def read_orders_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as file:
        return list(csv.DictReader(file))
```

Extract ma pobrac dane.

Nie licz tu revenue.

<!-- end_slide -->

# Validate: required fields

```python
REQUIRED_FIELDS = {"order_id", "status", "total_amount"}

has_required_fields = all(record.get(field) for field in REQUIRED_FIELDS)
```

Pytanie:

```text
Czy rekord bez order_id moze wejsc do transformacji?
```

Nie powinien.

<!-- end_slide -->

# Validate: Pydantic

```python
class OrderPayload(BaseModel):
  order_id: str
  status: str
  total_amount: float = Field(ge=0)
  source: str = "unknown"
```

Pydantic sprawdza raw `dict` z pliku albo API.

Tu odrzucasz:

```text
brak order_id
ujemny total_amount
tekst zamiast liczby
nieznany status
```

<!-- end_slide -->

# dataclass Order

```python
@dataclass(frozen=True)
class Order:
  order_id: str
  status: str
  total_amount: float
  source: str
```

Po walidacji nie nosimy dalej surowego `dict`.

Transformacje pracuja na jasnym typie: `Order`.

<!-- end_slide -->

# Transform

```python
def calculate_completed_revenue(records: list[Order]) -> float:
  revenue = 0.0
  for record in records:
    if record.is_completed:
      revenue = revenue + record.total_amount
  return revenue
```

Tu liczysz metryke na rekordach, ktore przeszly kontrakt.

<!-- end_slide -->

# Rejected records

```python
@dataclass(frozen=True)
class RejectedRecord:
  record: dict[str, Any]
  reason: str
```

Nie wystarczy powiedziec: "rekord byl zly".

Chcesz wiedziec:

```text
ktory rekord odpadl
dlaczego odpadl
```

<!-- end_slide -->

# Load

```python
def write_json_output(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
```

Load zapisuje wynik.

Dzieki temu mozna go pokazac reviewerowi albo downstream userowi.

<!-- end_slide -->

# Fajny przyklad interview

Pytanie:

```text
Jak testujesz pipeline, ktory normalnie czyta API?
```

Odpowiedz:

```text
Oddzielam funkcje transformacji od IO.
API payload zapisuje jako maly JSON fixture.
Testuje walidacje i transformacje bez prawdziwej uslugi.
Osobno testuje, ze kod obsluguje blad HTTP albo pusty payload.
```

<!-- end_slide -->

# Homework

Oddajesz:

```text
pipeline_workflow.py
test_pipeline_workflow.py
orders.csv
api_orders.json
pipeline_output.json
notes.md
interview_answer.md
```

Najwazniejszy test:

```text
Pydantic odrzuca bledny rekord,
dataclass Order reprezentuje poprawny rekord,
revenue liczy tylko accepted completed orders
```

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
Extract pobiera dane.
Validate sprawdza ksztalt przez Pydantic.
dataclass Order opisuje poprawny rekord.
Transform liczy metryki na accepted orders.
Load zapisuje wynik.
Testy powinny pokrywac bledny rekord i happy path.
```
