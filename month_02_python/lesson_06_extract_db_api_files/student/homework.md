# Praca domowa: Lekcja 06

## Cel

Masz zbudowac maly pipeline Python z kontraktem rekordu:

```text
extract -> validate with Pydantic -> dataclass records -> transform -> load
```

## Krok 0: przygotuj katalog

```bash
mkdir -p homework/lesson_06
cd homework/lesson_06
touch pipeline_workflow.py test_pipeline_workflow.py notes.md interview_answer.md
```

Skopiuj albo utworz male dane:

```text
orders.csv
api_orders.json
```

## Krok 1: extract

W `pipeline_workflow.py` napisz:

```python
def read_orders_csv(path: Path) -> list[dict[str, str]]:
    ...

def read_orders_api_payload(path: Path) -> list[dict[str, object]]:
    ...
```

API moze byc plikiem JSON. Nie potrzebujesz prawdziwej uslugi.

## Krok 2: validate

Najpierw zrob prosty required fields check:

```python
def validate_required_fields(records: list[dict[str, object]], required_fields: set[str]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    ...
```

Funkcja ma zwrocic:

```text
accepted_records, rejected_records
```

Potem dodaj Pydantic model:

```python
class OrderPayload(BaseModel):
    order_id: str
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"
```

W modelu znormalizuj status do lowercase i odrzuc status spoza listy:

```text
completed
cancelled
pending
refunded
```

## Krok 2b: dataclass

Dodaj rekord domenowy:

```python
@dataclass(frozen=True)
class Order:
    order_id: str
    status: str
    total_amount: float
    source: str
```

Dodaj tez rejected record:

```python
@dataclass(frozen=True)
class RejectedRecord:
    record: dict[str, object]
    reason: str
```

## Krok 3: transform

Dodaj:

```python
def normalize_order(record: dict[str, object]) -> dict[str, object]:
    ...

def validate_and_parse_orders(records: list[dict[str, object]]) -> tuple[list[Order], list[RejectedRecord]]:
    ...

def calculate_completed_revenue(records: list[Order]) -> float:
    ...

def calculate_completed_revenue_by_source(records: list[Order]) -> dict[str, float]:
    ...
```

Jesli dodasz `validate_and_parse_orders`, funkcja `normalize_order` moze juz nie byc potrzebna. To jest OK. Pydantic + dataclass przejmuja jej role.

## Krok 4: load

Dodaj:

```python
def write_json_output(payload: dict[str, object], path: Path) -> None:
    ...
```

## Krok 5: run_pipeline

Dodaj funkcje:

```python
def run_pipeline(input_path: Path, output_path: Path) -> dict[str, object]:
    ...
```

Wynik powinien zawierac:

```text
accepted_count
rejected_count
completed_revenue
revenue_by_source
accepted_orders
rejected_records z reason
```

## Krok 6: testy

W `test_pipeline_workflow.py` napisz testy:

1. CSV extract zwraca rekordy.
2. Walidacja odrzuca rekord bez `order_id`.
3. Pydantic odrzuca ujemny `total_amount`.
4. Pydantic odrzuca nieznany status.
5. Status jest normalizowany do lowercase.
6. Poprawny payload staje sie `Order` dataclass.
7. Revenue liczy tylko completed orders.
8. `run_pipeline` tworzy output JSON z accepted i rejected records.

## Krok 7: notes i interview

W `notes.md` odpowiedz:

```text
Gdzie konczy sie extract, a zaczyna transform?
Dlaczego walidacja jest osobnym krokiem?
Po co Pydantic w tym pipeline?
Czym rozni sie raw dict od dataclass Order?
Co zapisujesz w output JSON?
```

W `interview_answer.md` odpowiedz w 8-12 zdaniach:

```text
Jak uzywasz Pythona do prostego pipeline'u Data Engineering?
```
