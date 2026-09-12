# Praca domowa: Lekcja 09

## Cel

Masz zbudowac modul integracyjny laczacy trzy wzorce z lekcji:

```text
API fetch z paginacja -> serializacja do Avro -> upload na S3 (mock)
```

To jest produkcyjny wzorzec ingestii danych: pobieramy, serializujemy do binarnego formatu,
wgrywamy do data lake.

## Co i gdzie robisz

Tworzysz projekt z src layout:

```text
homework/lesson_09/
├── pyproject.toml
├── src/
│   └── ingestion/
│       ├── __init__.py
│       ├── api.py        <- fetch + pagination + retry
│       ├── serialize.py  <- Avro write/read
│       └── storage.py    <- upload (klient jako parametr)
└── tests/
    ├── conftest.py
    ├── test_api.py
    ├── test_serialize.py
    └── test_storage.py
```

## Krok 0: przygotuj projekt

```bash
mkdir -p homework/lesson_09/src/ingestion homework/lesson_09/tests
cd homework/lesson_09
touch src/ingestion/__init__.py src/ingestion/api.py src/ingestion/serialize.py src/ingestion/storage.py
touch tests/__init__.py tests/conftest.py tests/test_api.py tests/test_serialize.py tests/test_storage.py
pyenv local 3.13.0
poetry init --name lesson-09-ingestion --python "^3.13" --no-interaction
poetry add httpx fastavro boto3
poetry add --group dev pytest pytest-mock mypy ruff
```

## Krok 1: fetch z paginacja

W `api.py` napisz `fetch_all(base_url: str, client: httpx.Client) -> list[dict]`.

Wymagania:

- Petla while True z cursor-based pagination.
- Zatrzymuje sie gdy `next == None` w odpowiedzi.
- Wywoluje `response.raise_for_status()` przed `response.json()`.

Wskazowka: `data.get("next")` zwraca `None` gdy klucz nie istnieje.
To bezpieczniejsze niz `data["next"]` ktore podnosi `KeyError`.

Jak o tym myslec:

```text
Strona 1: get /orders             -> 25 rekordow + next = "cursor_abc"
Strona 2: get /orders?cursor=abc  -> 25 rekordow + next = "cursor_def"
Strona N: get /orders?cursor=xyz  -> 12 rekordow + next = None  <- stop
```

## Krok 2: retry z backoff

W `api.py` napisz `retryable_get(client, url, params, max_attempts, base_delay)`.

Wymagania:

```text
max_attempts = 4
retry tylko dla: 408, 429, 500, 502, 503, 504
brak retry dla: 400, 401, 403, 404
exponential backoff: delay = base_delay * 2^attempt
dodaj jitter: random.uniform(0.0, 0.2) do delay
```

Wskazowka: nie uzywaj `time.sleep` bezposrednio w petli — zaimportuj `time` i uzyj `time.sleep(delay)`.
Jitter zapobiega "thundering herd" — gdy 100 klientow pada i retry wszyscy naraz.

Jesli utkniesz: zacznij od wersji bez retry, ktora dziala poprawnie.
Potem dodaj petle z limitem prob.

## Krok 3: serializacja Avro

W `serialize.py` napisz:

- `ORDER_SCHEMA` — slownik opisujacy schemat Avro dla jednego zamowienia (minimum: `order_id`, `status`, `total_amount`).
- `to_avro(records: list[dict]) -> bytes` — serializuje rekordy do bajtow.
- `from_avro(data: bytes) -> list[dict]` — deserializuje bajty z powrotem do listy.

Wskazowka: `fastavro.parse_schema(SCHEMA_DICT)` przygotowuje schemat przed uzyciem.
`BytesIO` sluzy jako bufor w pamieci — nie zapisujesz na dysk.

Jak o tym myslec:

```text
records -> to_avro -> bytes -> przechowujesz/wysylasz/uploadujesz
bytes   -> from_avro -> records (te same co na wejsciu)
```

## Krok 4: upload S3

W `storage.py` napisz `upload_bytes(data: bytes, bucket: str, key: str, client) -> None`.

Wymaganie: klient jako parametr — nie tworzysz `boto3.client()` wewnatrz funkcji.

Wskazowka: gdy klient jest parametrem, w tescie podajesz `MagicMock` zamiast prawdziwego AWS.
To jest fundamentalny wzorzec testowalnosci integracji.

## Krok 5: testy

Napisz testy w odpowiednich plikach:

W `test_api.py`:

1. `fetch_all` zbiera rekordy z N stron (mock HTTP z `pytest-mock`).
2. `retryable_get` robi retry dla 429 i zatrzymuje sie po sukcesie.
3. `retryable_get` nie robi retry dla 400.
4. `retryable_get` podnosi wyjatek po wyczerpaniu limitu prob.

W `test_serialize.py`:

5. Roundtrip: `from_avro(to_avro(records)) == records`.

W `test_storage.py`:

6. `upload_bytes` wywoluje `client.put_object` z poprawnymi argumentami (MagicMock).

Wskazowka na mockowanie HTTP: uzyj `responses` albo `pytest-mock` z `mocker.patch`.
W `conftest.py` mozesz zdefiniowac fixture z gotowymi przykladowymi rekordami.

Jesli utkniesz na mockowaniu: zacznij od testu roundtrip Avro — on nie wymaga mocka.

## Krok 6: sprawdzenie jakosci kodu

Uruchom mypy i ruff:

```bash
cd homework/lesson_09
mypy src/
ruff check src/ tests/
```

Oba musza przejsc czysto przed oddaniem.

## Jak uruchomic

```bash
cd homework/lesson_09
pytest tests/ -v
mypy src/
ruff check src/ tests/
```

## Jak oddac prace przez GitHub

```bash
git checkout -b lesson-09-homework
git add homework/lesson_09
git commit -m "Add lesson 09 homework"
git push -u origin lesson-09-homework
```

W opisie PR napisz krotko:

```text
Co zrobilem:
Co bylo trudne:
Czego nie jestem pewien:
```

## Co oddac

```text
homework/lesson_09/
├── pyproject.toml
├── src/ingestion/ (wszystkie .py)
└── tests/ (wszystkie .py)
```

Nie commituj `.venv/`.

## Wersja ambitna

Tylko po zrobieniu minimum:

1. Dodaj `batch_size` do `fetch_all` ktory zatrzymuje sie po N rekordach (przydatne w testach).
2. Napisz `list_keys(bucket, prefix, client)` w `storage.py` i przetestuj go mockiem.
3. Dodaj `content_type="application/avro"` do `put_object` i sprawdz to w tescie.

## Checklista przed oddaniem

- [ ] Paginacja pobiera wszystkie strony az do `next == None`.
- [ ] Retry uzywa exponential backoff + jitter i ma limit prob.
- [ ] Retry dotyczy tylko transient errors (408/429/5xx).
- [ ] Avro roundtrip zachowuje wszystkie pola i typy.
- [ ] S3 upload uzywa klienta z parametru, nie tworzy `boto3.client()` wewnatrz.
- [ ] Testy przechodza przez `pytest`.
- [ ] `mypy` i `ruff` przechodza czysto.
