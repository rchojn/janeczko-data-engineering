---
title: Lekcja 06 - dataclass i Pydantic w pipeline Python
author: Data Engineering Course
date: 2026-08-14
---

# dataclass i Pydantic

W Python Data Engineering pipeline

```text
raw dict -> Pydantic validation -> dataclass Order -> metrics -> output
```

Cel: zrozumiec roznice miedzy zwykla klasa, `dataclass` i Pydantic.

<!-- end_slide -->

# Problem

Dane z pliku albo API przychodza jako raw payload.

Najczesciej widzisz cos takiego:

```python
record = {
    "order_id": "1001",
    "status": "Completed",
    "total_amount": "120.50",
    "source": "api",
}
```

To jest `dict`.

Pytanie: czy mozemy mu ufac?

<!-- end_slide -->

# dict

`dict` przechowuje dane jako klucz -> wartosc.

```python
record["status"]
record["total_amount"]
```

Plusy:

```text
prosty
naturalny format po CSV/JSON
latwy do wypisania
```

Minus:

```text
nie pokazuje kontraktu rekordu
```

<!-- end_slide -->

# Problem z dict

Ten kod dziala tylko wtedy, gdy dane sa poprawne:

```python
amount = float(record["total_amount"])
```

Ale payload moze byc taki:

```python
{"order_id": "1002", "total_amount": "not-a-number"}
```

Albo taki:

```python
{"status": "completed", "total_amount": "120.50"}
```

Brakuje `order_id`.

<!-- end_slide -->

# Zwykla klasa

Mozesz napisac zwykla klase:

```python
class Order:
    def __init__(self, order_id: str, status: str, total_amount: float) -> None:
        self.order_id = order_id
        self.status = status
        self.total_amount = total_amount
```

To dziala.

Ale dla prostych rekordow jest duzo powtarzalnego kodu.

<!-- end_slide -->

# Co daje zwykla klasa

Zwykla klasa jest dobra, gdy obiekt ma zachowanie.

Przyklad:

```python
class Order:
    def __init__(self, order_id: str, status: str, total_amount: float) -> None:
        self.order_id = order_id
        self.status = status
        self.total_amount = total_amount

    def is_completed(self) -> bool:
        return self.status == "completed"
```

Klasa = dane + zachowanie.

<!-- end_slide -->

# Minus zwyklej klasy

Dla prostych rekordow piszesz duzo boilerplate:

```text
__init__
self.field = field
__repr__
__eq__
czasem immutable handling
```

Boilerplate to kod, ktory musisz napisac, ale nie niesie duzo logiki biznesowej.

<!-- end_slide -->

# dataclass

`dataclass` generuje nudna czesc za Ciebie.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str
```

To jest dobry format dla poprawnego rekordu w pipeline.

<!-- end_slide -->

# class vs dataclass

```text
class
  piszesz __init__ sam
  dobra, gdy obiekt ma wiecej zachowania
  wiecej kodu dla prostych rekordow

dataclass
  Python generuje __init__, repr, eq
  dobra do struktur danych
  mniej kodu, bardziej czytelny kontrakt
```

W pipeline czesto chcesz `dataclass` dla rekordu po walidacji.

<!-- end_slide -->

# dataclass z metoda

`dataclass` moze miec metody.

```python
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

To nadal jest proste i czytelne.

<!-- end_slide -->

# frozen=True

```python
@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
```

`frozen=True` znaczy: po utworzeniu nie zmieniaj obiektu.

Dlaczego to pomaga?

```text
rekord po walidacji jest stabilny
trudniej przypadkiem zmienic status w srodku pipeline
latwiej debugowac transformacje
```

<!-- end_slide -->

# Ale dataclass nie wystarczy

`dataclass` nie jest mocna walidacja raw inputu.

```python
Order(
    order_id="1001",
    status="unknown",
    total_amount=-10.0,
    source="api",
)
```

To technicznie moze sie utworzyc.

Ale biznesowo rekord jest podejrzany.

<!-- end_slide -->

# Pydantic

Pydantic waliduje raw payload w runtime.

```python
from pydantic import BaseModel, Field

class OrderPayload(BaseModel):
    order_id: str
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"
```

Pydantic sprawdza dane wtedy, gdy przychodza z zewnatrz.

<!-- end_slide -->

# Co sprawdza Pydantic

Dla `OrderPayload`:

```text
order_id musi istniec
status musi byc tekstem
total_amount musi dac sie zamienic na float
total_amount musi byc >= 0
source ma default "unknown"
```

To jest kontrakt wejscia do pipeline.

<!-- end_slide -->

# Pydantic validator

Mozesz dopisac regule biznesowa.

```python
ALLOWED_STATUSES = {"completed", "cancelled", "pending", "refunded"}

@field_validator("status")
@classmethod
def normalize_and_validate_status(cls, value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in ALLOWED_STATUSES:
        raise ValueError("unknown status")
    return normalized
```

Tu status jest normalizowany i sprawdzany.

<!-- end_slide -->

# Pydantic vs dataclass

```text
Pydantic
  granica pipeline
  sprawdza raw dict z CSV/JSON/API
  mowi: accepted albo rejected

dataclass
  srodek pipeline
  reprezentuje poprawny rekord
  wygodny do transformacji i metryk
```

To sa rozne narzedzia.

Nie musisz wybierac jednego.

<!-- end_slide -->

# Pelny flow

```text
CSV/JSON
  |
  v
raw dict
  |
  v
OrderPayload.model_validate(record)
  |
  v
Order dataclass
  |
  v
calculate_completed_revenue(orders)
  |
  v
pipeline_output.json
```

To jest realny wzorzec pipeline.

<!-- end_slide -->

# Accepted i rejected

Pipeline powinien rozdzielic rekordy:

```python
accepted: list[Order] = []
rejected: list[RejectedRecord] = []
```

Rejected record powinien miec powod:

```python
@dataclass(frozen=True)
class RejectedRecord:
    record: dict[str, object]
    reason: str
```

Bez reason nie wiesz, co naprawic.

<!-- end_slide -->

# Przyklad accepted

Raw payload:

```python
{"order_id": "1001", "status": " Completed ", "total_amount": "120.50"}
```

Po Pydantic:

```python
OrderPayload(order_id="1001", status="completed", total_amount=120.5, source="unknown")
```

Po konwersji:

```python
Order(order_id="1001", status="completed", total_amount=120.5, source="unknown")
```

<!-- end_slide -->

# Przyklad rejected

Raw payload:

```python
{"order_id": "1006", "status": "completed", "total_amount": "-12.00"}
```

Pydantic odrzuca:

```text
total_amount: Input should be greater than or equal to 0
```

Do outputu zapisujesz:

```text
record + reason
```

<!-- end_slide -->

# Metryka na dataclass

```python
def calculate_completed_revenue(records: list[Order]) -> float:
    revenue = 0.0
    for record in records:
        if record.is_completed:
            revenue = revenue + record.total_amount
    return revenue
```

Ta funkcja nie martwi sie juz o raw JSON.

Dostaje tylko poprawne `Order`.

<!-- end_slide -->

# Dlaczego to jest wazne w DE

Data Engineering to nie tylko policzenie sumy.

Musisz wiedziec:

```text
czy dane przyszly w dobrym ksztalcie,
ile rekordow zaakceptowano,
ile odrzucono,
dlaczego odrzucono,
czy metryki licza sie tylko na accepted records.
```

To buduje zaufanie do pipeline.

<!-- end_slide -->

# Co testowac

Testy powinny sprawdzac:

```text
valid payload przechodzi
missing order_id jest rejected
negative amount jest rejected
unknown status jest rejected
status robi sie lowercase
accepted payload staje sie Order dataclass
revenue liczy tylko completed orders
output JSON ma accepted_count i rejected_count
```

To sa testy kontraktu, nie tylko skladni.

<!-- end_slide -->

# Interview answer

Pytanie:

```text
How would you use dataclasses and Pydantic in a Python data pipeline?
```

Odpowiedz:

```text
I use Pydantic at the boundary of the pipeline to validate raw payloads from files or APIs.
If the payload is valid, I convert it into a dataclass that represents the domain record.
Transformations and metrics operate on dataclasses, not raw dictionaries.
Invalid payloads are written to rejected records with error reasons.
This keeps validation, domain modeling and business logic separate.
```

<!-- end_slide -->

# Najkrotszy wzorzec

```text
raw dict
  dane z zewnatrz, nie ufamy

Pydantic model
  waliduje input

dataclass
  reprezentuje poprawny rekord w kodzie

transform functions
  licza metryki na accepted records

rejected records
  pokazuja, co i dlaczego odpadlo
```

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
Zwykla klasa daje dane i zachowanie, ale wymaga wiecej kodu.
dataclass jest lepszy do prostych rekordow po walidacji.
Pydantic waliduje raw dane z pliku, API albo JSON.
W pipeline uzywam Pydantic na wejsciu, dataclass w srodku.
Rejected records musza miec reason.
```
