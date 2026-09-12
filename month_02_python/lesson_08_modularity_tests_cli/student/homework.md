# Praca domowa: Lekcja 08

## Cel

Masz zbudowac mini projekt Python ETL, ktory dziala jak prawdziwe narzedzie CLI.

Nie wystarczy, ze skrypt dziala raz lokalnie. Pipeline musi dac sie uruchomic parametrami,
miec testy, logi i runbook — tak jak w produkcji.

## Co i gdzie robisz

Tworzysz caly projekt w osobnym katalogu:

```text
homework/lesson_08/
├── pyproject.toml
├── README.md
├── runbook.md
├── data/
│   └── orders.json
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── cli.py
│       ├── extract.py
│       ├── transform.py
│       ├── load.py
│       └── models.py
└── tests/
    └── test_pipeline.py
```

Wzorzec do nauki masz w `student/lab/mini_etl_cli.py` i rozwiazaniu mentora.
Nie kopiujesz gotowego kodu — budujesz structure samodzielnie.

## Krok 0: przygotuj projekt

```bash
mkdir -p homework/lesson_08/src/pipeline homework/lesson_08/tests homework/lesson_08/data
cd homework/lesson_08
touch src/pipeline/__init__.py src/pipeline/cli.py
touch src/pipeline/extract.py src/pipeline/transform.py src/pipeline/load.py src/pipeline/models.py
touch tests/test_pipeline.py README.md runbook.md
cp ../../student/lab/data/orders.json data/
pyenv local 3.13.0
poetry init --name lesson-08-pipeline --python "^3.13" --no-interaction
poetry add --group dev pytest mypy ruff
```

Wskazowka: `src/` layout sprawia, ze kod jest importowalny przez `from pipeline.extract import ...`.
Bez `src/` i `__init__.py` import nie bedzie dzialal.

Jesli utkniesz na imporcie: sprawdz czy masz `src/pipeline/__init__.py` (pusty plik).
Potem sprawdz czy uruchamiasz pytest z katalogu `homework/lesson_08`.

## Krok 1: models.py

W `models.py` napisz dataclassy opisujace dane:

- `Order` — rekord po normalizacji: `order_id`, `status`, `total_amount`.
- Mozesz dodac property `is_completed` dla czystszej logiki w transform.

## Krok 2: extract.py

Napisz funkcje `read_json_records(path: Path) -> list[dict[str, object]]`.

Wymaganie: funkcja tylko czyta plik i zwraca surowe rekordy. Nie liczy metryk.

Wskazowka: uzyj `pathlib.Path.read_text()` i `json.loads()`.
Obsluz `FileNotFoundError` i podaj czytelny komunikat zamiast traceback z Python internals.

## Krok 3: transform.py

Napisz dwie czyste funkcje transformacji:

- `normalize_records(records: list[dict]) -> list[Order]` — normalizuje status do lowercase i buduje `Order`.
- `calculate_completed_revenue(records: list[Order]) -> float` — liczy revenue dla statusu `completed`.

Wymaganie: funkcje przyjmuja dane przez argument i zwracaja wynik. Nie czytaja plikow.

## Krok 4: load.py

Napisz `write_json(payload: dict[str, object], path: Path) -> None`.

Wymaganie: tworzy katalog wyjsciowy jesli nie istnieje.

## Krok 5: cli.py

Napisz CLI przez `argparse` z dwoma parametrami: `--input` i `--output`.

Pipeline uruchamiany tak:

```bash
python -m pipeline.cli --input data/orders.json --output output/result.json
```

Dodaj logging zamiast print:

```text
INFO  Pipeline started
INFO  Loaded N records
INFO  Wrote output to PATH
ERROR Pipeline failed: REASON
```

Wskazowka: uzyj `logging.basicConfig(level=logging.INFO)` i `logger = logging.getLogger(__name__)`.
Logging daje poziomy i timestamp — `print` tego nie ma.

## Krok 6: retry

W jednej funkcji (read albo write) dodaj prosty retry z limitem prob.

Wymaganie: retry tylko dla bledow przejsciowych (np. `OSError`), nie dla zlego inputu.

Wskazowka: retry bez limitu to nieskonczona petla. Zawsze ustaw `max_attempts`.

## Krok 7: testy

W `tests/test_pipeline.py` napisz minimum cztery testy:

1. `normalize_records` zmienia status na lowercase.
2. `calculate_completed_revenue` liczy tylko completed orders.
3. `write_json` zapisuje plik i mozna go odczytac.
4. `read_json_records` podnosi czytelny blad dla brakujacego pliku.

Wskazowka: testuj funkcje bezposrednio, nie przez CLI.
CLI to tylko warstwa uruchamiania — logika biznesowa siedzi w extract/transform/load.

## Krok 8: runbook.md

W `runbook.md` odpowiedz krotko na 5 pytan:

```text
1. Jak uruchomic pipeline od zera?
2. Gdzie sa pliki wejsciowe i wyjsciowe?
3. Jak sprawdzic logi?
4. Jak zrobic rerun jesli pipeline padnie?
5. Jakie sa najczestsze przyczyny awarii?
```

Runbook ma byc napisany dla osoby, ktora nie zna Twojego kodu.
Jeden krok = jedno polecenie albo jedno zdanie co sprawdzic.

## Krok 9: uruchomienie

Sprawdz, ze wszystko dziala:

```bash
cd homework/lesson_08
python -m pipeline.cli --input data/orders.json --output output/result.json
pytest tests/ -v
```

Oba polecenia maja zakonczyc sie bez bledow.

## Jak oddac prace przez GitHub

```bash
git checkout -b lesson-08-homework
git add homework/lesson_08
git commit -m "Add lesson 08 homework"
git push -u origin lesson-08-homework
```

W opisie PR napisz krotko:

```text
Co zrobilem:
Co bylo trudne:
Czego nie jestem pewien:
```

## Co oddac

```text
homework/lesson_08/
├── pyproject.toml
├── README.md
├── runbook.md
├── data/orders.json
├── src/pipeline/ (wszystkie pliki .py)
└── tests/test_pipeline.py
```

Nie commituj `output/` ani `.venv/`.

## Wersja ambitna

Tylko po zrobieniu minimum:

1. Dodaj `--dry-run` do CLI ktory pokazuje co zostaloby zapisane, ale nie zapisuje.
2. Dodaj `--log-level DEBUG/INFO/ERROR` jako argument CLI.
3. Napisz test sprawdzajacy ze retry nie przekracza limitu prob.

## Checklista przed oddaniem

- [ ] Pipeline uruchamia sie przez `python -m pipeline.cli --input ... --output ...`.
- [ ] Input i output ida jako parametry, nie sa hardcodowane.
- [ ] Testy pokrywaja normalizacje, revenue i zapis pliku.
- [ ] Logging uzywa `logging`, nie `print`.
- [ ] Retry ma limit prob.
- [ ] `runbook.md` odpowiada na wszystkie 5 pytan.
- [ ] `README.md` tlumaczy jak uruchomic projekt od zera.
