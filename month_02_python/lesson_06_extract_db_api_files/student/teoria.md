# Teoria: Lekcja 06 - Python Pipeline Workflow, Pydantic i dataclass

## Cel materiału

Ten materiał pokazuje, jak przejść od prostych funkcji z lekcji 05 do małego pipeline'u Data Engineering.

W lekcji 05 program liczył metrykę na liście rekordów. W lekcji 06 dokładamy strukturę pracy, która jest bliższa realnym projektom:

```text
extract -> validate -> domain model -> transform -> load
```

Po tej lekcji uczestnik powinien umieć:

```text
czytać dane z CSV i JSON,
oddzielić pobieranie danych od logiki biznesowej,
sprawdzić raw payload przez Pydantic,
zamienić poprawny rekord na dataclass,
zapisać rejected records z powodem,
policzyć metryki na accepted records,
zapisać wynik pipeline'u do JSON,
przetestować happy path i błędne rekordy.
```

## Kontekst ekosystemu

> Czytaj to pierwsze.

W praktyce Data Engineering dane rzadko są idealne. Nawet mały pipeline musi odpowiedzieć na pytania:

```text
Skąd przyszły dane?
Czy payload ma oczekiwany kształt?
Co robimy z błędnym rekordem?
Czy metryki liczymy tylko na poprawnych danych?
Czy output da się odtworzyć?
```

W tej lekcji używamy trzech reprezentacji danych:

| Reprezentacja | Gdzie występuje | Rola |
|---|---|---|
| `dict` | zaraz po CSV/JSON | raw payload, któremu jeszcze nie ufamy |
| Pydantic `BaseModel` | na granicy pipeline'u | walidacja pól, typów i reguł |
| `dataclass` | wewnątrz pipeline'u | poprawny rekord używany przez transformacje |

## ELI5

Pipeline to uporządkowany proces pracy z danymi.

Najprostszy obraz:

```text
weź dane -> sprawdź dane -> uporządkuj dane -> policz wynik -> zapisz wynik
```

Pydantic jest bramką przy wejściu. Sprawdza, czy rekord wygląda tak, jak powinien.

`dataclass` jest czystym rekordem w środku programu. Używamy go po walidacji, żeby dalszy kod był czytelny i nie musiał ciągle pracować na surowych słownikach.

## First Principles

Pipeline ma dwie grupy problemów:

```text
1. Problemy z danymi wejściowymi
2. Problemy z logiką przetwarzania
```

Przykłady problemów z wejściem:

```text
brakuje order_id,
total_amount jest tekstem "not-a-number",
kwota jest ujemna,
status ma nieznaną wartość.
```

Przykłady problemów z logiką:

```text
revenue liczy cancelled orders,
transformacja miesza się z odczytem pliku,
output nadpisuje się w niekontrolowany sposób,
testy nie pokrywają błędnych rekordów.
```

Dlatego rozdzielamy kroki pipeline'u.

## Profesjonalny flow lekcji

```text
CSV / JSON files
  |
  v
extract: read raw records as dict
  |
  v
validate: Pydantic checks fields, types and rules
  |
  v
domain model: dataclass Order
  |
  v
transform: calculate metrics on accepted orders
  |
  v
load: write output JSON with accepted/rejected summary
```

Ten flow jest mały, ale przypomina prawdziwą strukturę pipeline'u.

## Extract

Extract ma pobrać dane i zwrócić raw records.

```python
def read_orders_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as file:
        return list(csv.DictReader(file))
```

Ważna zasada:

```text
Extract nie liczy revenue.
Extract nie naprawia biznesowo danych.
Extract tylko pobiera payload i przekazuje go dalej.
```

Dzięki temu łatwiej testować transformacje bez prawdziwego API albo bazy.

## Raw dict

Po odczycie CSV albo JSON rekord jest zwykłym słownikiem:

```python
record = {
    "order_id": "1001",
    "status": " Completed ",
    "total_amount": "120.50",
    "source": "csv",
}
```

To jest raw payload. Na tym etapie nie zakładamy jeszcze, że rekord jest poprawny.

Ryzyka raw `dict`:

```text
pole może nie istnieć,
typ może być inny niż oczekiwany,
status może wymagać normalizacji,
kwota może być ujemna,
kod może literówką odwołać się do złego klucza.
```

## Pydantic jako walidacja wejścia

Pydantic sprawdza rekord w runtime, czyli wtedy, gdy dane faktycznie przychodzą do programu.

```python
class OrderPayload(BaseModel):
    order_id: str
    status: str
    total_amount: float = Field(ge=0)
    source: str = "unknown"
```

Ten model mówi:

```text
order_id jest wymagany,
status jest wymagany,
total_amount ma być liczbą,
total_amount musi być >= 0,
source ma wartość domyślną unknown.
```

## Validator statusu

Walidacja typu nie wystarcza, bo status może być tekstem, ale nadal mieć złą wartość.

```python
ALLOWED_STATUSES = {"completed", "cancelled", "pending", "refunded"}

@field_validator("status")
@classmethod
def normalize_and_validate_status(cls, value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in ALLOWED_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_STATUSES))
        raise ValueError(f"status must be one of: {allowed}")
    return normalized
```

Ten validator robi dwie rzeczy:

```text
normalizuje status,
odrzuca status spoza kontraktu.
```

## dataclass jako rekord domenowy

Po walidacji chcemy pracować na jasnym typie, nie na raw `dict`.

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

`dataclass` jest dobry do reprezentowania prostych rekordów danych.

`frozen=True` oznacza, że po utworzeniu obiektu nie zmieniamy go przypadkiem w środku pipeline'u.

## Pydantic vs dataclass

To są różne narzędzia.

| Narzędzie | Gdzie używać | Po co |
|---|---|---|
| `dict` | na wejściu z CSV/JSON/API | reprezentuje raw payload |
| Pydantic | na granicy pipeline'u | sprawdza, czy payload jest poprawny |
| `dataclass` | po walidacji | daje czytelny rekord dla transformacji |

Wzorzec:

```text
Nie ufaj raw dict.
Sprawdź go przez Pydantic.
Dopiero potem zamień na dataclass.
```

## Accepted i rejected records

Pipeline nie powinien cicho pomijać błędnych rekordów.

```python
@dataclass(frozen=True)
class RejectedRecord:
    record: dict[str, Any]
    reason: str
```

Rejected record powinien odpowiedzieć na dwa pytania:

```text
który rekord odpadł?
dlaczego odpadł?
```

Przykłady powodów:

```text
missing required field
total_amount: Input should be greater than or equal to 0
status: Value error, status must be one of: cancelled, completed, pending, refunded
```

## Transform

Transformacja pracuje na accepted records, czyli na `list[Order]`.

```python
def calculate_completed_revenue(records: list[Order]) -> float:
    revenue = 0.0
    for record in records:
        if record.is_completed:
            revenue = revenue + record.total_amount
    return revenue
```

Ta funkcja nie sprawdza już, czy `total_amount` jest liczbą. To zostało załatwione wcześniej przez Pydantic.

To jest istota rozdzielenia odpowiedzialności.

## Load

Load zapisuje wynik pipeline'u.

```python
def write_json_output(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
```

Output powinien zawierać nie tylko metrykę, ale też kontekst jakości danych:

```text
accepted_count,
rejected_count,
completed_revenue,
revenue_by_source,
accepted_orders,
rejected_records.
```

## Socratic Questions

**Czy Pydantic zastępuje testy?**

Nie. Pydantic sprawdza pojedynczy payload według kontraktu. Testy sprawdzają, czy cały pipeline zachowuje się poprawnie: accepted/rejected counts, revenue, output JSON i przypadki brzegowe.

**Czy `dataclass` zastępuje Pydantic?**

Nie. `dataclass` dobrze opisuje poprawny rekord, ale sam nie jest wystarczającą walidacją raw danych z zewnątrz.

**Dlaczego transformacja nie powinna czytać pliku?**

Bo wtedy trudno ją testować. Transformacja powinna przyjmować dane jako argument i zwracać wynik. Odczyt pliku to osobny krok extract.

**Dlaczego rejected records są ważne?**

Bo bez nich nie wiesz, czy pipeline odrzucił 1 rekord, 1000 rekordów, czy połowę danych. Rejected records pozwalają debugować jakość danych.

**Kiedy retry ma sens?**

Retry ma sens dla błędów przejściowych, np. problemu z plikiem, API albo siecią. Retry nie naprawi złego payloadu, np. `total_amount = "not-a-number"`.

## STALY PATTERN - zapamietaj to

```text
PYTHON DATA ENGINEERING PIPELINE - staly pattern

=== Extract ===
raw_records = read_orders_csv(path) + read_orders_api_payload(path)
# Extract pobiera dane jako list[dict]. Nie liczy metryk.

=== Validate Boundary ===
payload = OrderPayload.model_validate(record)
# Pydantic sprawdza required fields, typy, zakresy i status.

=== Domain Record ===
order = Order(
    order_id=payload.order_id,
    status=payload.status,
    total_amount=payload.total_amount,
    source=payload.source,
)
# Po walidacji pracujemy na dataclass, nie na raw dict.

=== Rejects ===
RejectedRecord(record=record, reason="...")
# Każdy odrzucony rekord ma powód odrzucenia.

=== Transform ===
completed_revenue = calculate_completed_revenue(accepted_orders)
# Metryki liczymy tylko na accepted records.

=== Load ===
write_json_output(result.to_output_payload(), output_path)
# Output zawiera metryki oraz accepted/rejected summary.

CHECKLIST:
[ ] Czy extract nie miesza się z transformacją?
[ ] Czy Pydantic waliduje raw payload?
[ ] Czy status jest normalizowany i sprawdzany?
[ ] Czy poprawny payload zmienia się w dataclass Order?
[ ] Czy rejected records mają reason?
[ ] Czy metryki liczą tylko accepted records?
[ ] Czy output zawiera accepted_count i rejected_count?
[ ] Czy testy pokrywają błędne rekordy?
```

## Typowe błędy i jak je rozpoznać

| Błąd | Objaw | Lepszy wzorzec |
|---|---|---|
| Liczenie metryk w extract | Funkcja robi za dużo rzeczy | Extract tylko pobiera dane |
| Praca na raw `dict` w całym pipeline | Literówki i brak jasnego kontraktu | Pydantic na wejściu, dataclass w środku |
| Ciche pomijanie błędów | Nie wiadomo, ile rekordów odpadło | `RejectedRecord` z `reason` |
| Brak testu dla błędnego rekordu | Pipeline działa tylko dla happy path | Test missing field, wrong status, negative amount |
| Retry na zły payload | Pipeline powtarza błąd bez sensu | Retry tylko dla błędów przejściowych |

## Minimalny standard oddania

Kod lekcji 06 powinien spełniać te wymagania:

```text
CSV i JSON są czytane w osobnych funkcjach,
raw records są walidowane przez Pydantic,
poprawne rekordy są reprezentowane przez dataclass Order,
błędne rekordy trafiają do rejected records z reason,
metryki są liczone tylko na accepted records,
output JSON zawiera metryki i summary jakości danych,
testy pokrywają happy path i błędne rekordy.
```

## Krótka odpowiedź interview

Pytanie:

```text
How would you structure a small Python data pipeline?
```

Odpowiedź:

```text
I separate the pipeline into extract, validation, domain modeling, transformation and load steps. Raw records from CSV or API are represented as dictionaries, but I do not trust them directly. I validate them at the pipeline boundary with Pydantic. Valid payloads are converted into dataclass records used by transformation functions. Invalid records are written to rejected records with error reasons. Metrics are calculated only on accepted records, and the output includes both business metrics and quality summary.
```
